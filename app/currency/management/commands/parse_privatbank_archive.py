import requests
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from currency import consts
from currency import model_choices as mch

from currency.models import Rate, Source
from currency.tasks import round_currency


class Command(BaseCommand):
    help = 'Parse PrivatBank Rate archive'      # noqa

    def handle(self, *args, **options):

        source = Source.objects.get_or_create(
            code_name=consts.CODE_NAME_PRIVATBANK,
            defaults={'name': 'PrivatBank'},
        )[0]
        available_currency_type = {
            'USD': mch.TYPE_USD,
            'EUR': mch.TYPE_EUR,
        }
        start = datetime.now().date()
        days_ago = 0

        while True:
            date_ = start - timedelta(days=days_ago)
            days_ago += 1

            base_url = "https://api.privatbank.ua/p24api/exchange_rates"
            params = {
                'json': '',
                'date': date_.strftime("%d.%m.%Y"),
            }
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            rates = filter(
                lambda item: item['baseCurrency'] == 'UAH' and item.get('currency') in available_currency_type,
                response.json()['exchangeRate'],
            )

            if not rates:
                break

            for rate in rates:
                currency_type = available_currency_type[rate['currency']]
                sale = round_currency(rate['saleRateNB'])
                buy = round_currency(rate['purchaseRateNB'])
                if not Rate.objects.filter(created__date=date_, source=source, type=currency_type,).exists():
                    rate_obj = Rate.objects.create(
                        created=date_,
                        sale=sale,
                        buy=buy,
                        source=source,
                        type=currency_type,
                    )
                    rate_obj.created = date_
                    rate_obj.save(update_fields=('created',))
