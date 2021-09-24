from celery import shared_task
import requests
from decimal import Decimal
from currency import model_choices as mch


def round_currency(num):
    return Decimal(num).quantize(Decimal('.01'))


@shared_task
def parse_privatbank():
    from currency.models import Rate

    privatbank_currency_url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
    response = requests.get(privatbank_currency_url)
    response.raise_for_status()

    rates = response.json()
    source = 'privatbank'
    # available_currency_type = ('USD', 'EUR')
    available_currency_type = {
        'USD': mch.TYPE_USD,
        'EUR': mch.TYPE_EUR,
    }

    for rate in rates:
        currency_type = rate['ccy']
        if currency_type in available_currency_type:

            sale = round_currency(rate['sale'])
            buy = round_currency(rate['buy'])
            c_t = available_currency_type[currency_type]

            last_rate = Rate.objects.filter(
                type=c_t,
                source=source,
            ).order_by('created').last()

            if (
                    last_rate is None or
                    last_rate.sale != sale or
                    last_rate.buy != buy
            ):
                Rate.objects.create(
                    type=c_t,
                    sale=sale,
                    buy=buy,
                    source=source,
                )
