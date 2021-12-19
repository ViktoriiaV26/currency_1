from celery import shared_task
import requests
from decimal import Decimal
from django.conf import settings
from django.core.mail import send_mail

from currency import consts
from currency import model_choices as mch
from bs4 import BeautifulSoup


def round_currency(num):
    return Decimal(num).quantize(Decimal('.01'))


@shared_task
def contact_us(subject, message):
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [settings.SUPPORT_EMAIL],
        fail_silently=False,
    )


@shared_task
def parse_privatbank():
    from currency.models import Rate, Source

    privatbank_currency_url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
    response = requests.get(privatbank_currency_url)
    response.raise_for_status()

    rates = response.json()
    source = Source.objects.get_or_create(
        code_name=consts.CODE_NAME_PRIVATBANK,
        defaults={'name': 'PrivatBank'},
    )[0]
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


@shared_task
def parse_monobank():
    from currency.models import Rate, Source

    monobank_currency_url = 'https://api.monobank.ua/bank/currency'
    response = requests.get(monobank_currency_url)
    response.raise_for_status()

    rates = response.json()
    source = Source.objects.get_or_create(
        code_name=consts.CODE_NAME_MONOBANK,
        defaults={'name': 'MonoBank'},
    )[0]
    available_currency_type = {
        840: mch.TYPE_USD,
        978: mch.TYPE_EUR,
    }

    for rate in rates:
        currency_type = rate['currencyCodeA']

        currency_type_UAH = rate['currencyCodeB']   # 980 - UAH

        if currency_type_UAH == 980:
            if currency_type in available_currency_type:
                sale = round_currency(rate['rateSell'])
                buy = round_currency(rate['rateBuy'])
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


@shared_task
def parse_vkurse():
    from currency.models import Rate, Source

    vkurse_currency_url = 'http://vkurse.dp.ua/course.json'
    response = requests.get(vkurse_currency_url)
    response.raise_for_status()

    rates = response.json()
    source = Source.objects.get_or_create(
        code_name=consts.CODE_NAME_VKURSE,
        defaults={'name': 'Vkurse'},
    )[0]

    available_currency_type = {
        'Dollar': mch.TYPE_USD,
        'Euro': mch.TYPE_EUR,
    }

    for currency_type, rate in rates.items():
        if currency_type not in available_currency_type:
            continue
        sale = rate['sale']
        buy = rate['buy']
        c_t = available_currency_type[currency_type]

        last_rate = Rate.objects.filter(
            type=c_t,
            source=source,
        ).order_by('created').last()

        if (
                last_rate is None or
                last_rate.sale != round_currency(sale) or
                last_rate.buy != round_currency(buy)
        ):
            Rate.objects.create(
                type=c_t,
                sale=sale,
                buy=buy,
                source=source,
            )


@shared_task
def parse_alfabank():
    from currency.models import Rate, Source

    alfa_currency_url = 'https://old.alfabank.ua/'
    response = requests.get(alfa_currency_url)
    response.raise_for_status()
    source = Source.objects.get_or_create(
        code_name=consts.CODE_NAME_ALFABANK,
        defaults={'name': 'AlfaBank'},
    )[0]

    soup = BeautifulSoup(response.text, 'html.parser')

    type_usd = mch.TYPE_USD
    type_eur = mch.TYPE_EUR

    usd_buy = soup.find("span", {"data-currency": "USD_BUY"}).text.strip()
    usd_sale = soup.find("span", {"data-currency": "USD_SALE"}).text.strip()

    last_rate = Rate.objects.filter(
        type=type_usd,
        source=source,
    ).order_by('created').last()

    if (
            last_rate is None or
            last_rate.sale != round_currency(usd_sale) or
            last_rate.buy != round_currency(usd_buy)
    ):
        Rate.objects.create(
            type=mch.TYPE_USD,
            sale=usd_sale,
            buy=usd_buy,
            source=source,
        )
    eur_buy = soup.find("span", {"data-currency": "EUR_BUY"}).text.strip()
    eur_sale = soup.find("span", {"data-currency": "EUR_SALE"}).text.strip()

    last_rate = Rate.objects.filter(
        type=type_eur,
        source=source,
    ).order_by('created').last()

    if (
            last_rate is None or
            last_rate.sale != round_currency(eur_sale) or
            last_rate.buy != round_currency(eur_buy)
    ):
        Rate.objects.create(
            type=mch.TYPE_EUR,
            sale=eur_sale,
            buy=eur_buy,
            source=source,
        )


@shared_task
def parse_oschad():
    from currency.models import Rate, Source

    oschad_currency_url = 'https://www.oschadbank.ua/currency-rate'
    response = requests.get(oschad_currency_url)
    response.raise_for_status()
    source = Source.objects.get_or_create(
        code_name=consts.CODE_NAME_OSCHADBANK,
        defaults={'name': 'OschadBank'},
    )[0]

    soup = BeautifulSoup(response.text, 'html.parser')

    type_usd = mch.TYPE_USD
    type_eur = mch.TYPE_EUR

    usd_buy = soup.findAll('span', {'class': ["heading-block-currency-rate__table-txt body-regular"]})[9].get_text()
    usd_sale = soup.findAll('span', {'class': ["heading-block-currency-rate__table-txt body-regular"]})[10].get_text()

    last_rate = Rate.objects.filter(
        type=type_usd,
        source=source,
    ).order_by('created').last()

    if (
            last_rate is None or
            last_rate.sale != round_currency(usd_sale) or
            last_rate.buy != round_currency(usd_buy)
    ):
        Rate.objects.create(
            type=type_usd,
            sale=usd_sale,
            buy=usd_buy,
            source=source,
        )

    eur_buy = soup.findAll('span', {'class': ["heading-block-currency-rate__table-txt body-regular"]})[15].get_text()
    eur_sale = soup.findAll('span', {'class': ["heading-block-currency-rate__table-txt body-regular"]})[16].get_text()

    last_rate = Rate.objects.filter(
        type=type_eur,
        source=source,
    ).order_by('created').last()

    if (
            last_rate is None or
            last_rate.sale != round_currency(eur_sale) or
            last_rate.buy != round_currency(eur_buy)
    ):
        Rate.objects.create(
            type=type_eur,
            sale=eur_sale,
            buy=eur_buy,
            source=source,
        )


@shared_task
def parse_universal():
    from currency.models import Rate, Source

    universal_currency_url = 'https://www.universalbank.com.ua/ru'
    response = requests.get(universal_currency_url)
    response.raise_for_status()
    source = Source.objects.get_or_create(
        code_name=consts.CODE_NAME_UNIVERSALBANK,
        defaults={'name': 'UniversalBank'},
    )[0]

    soup = BeautifulSoup(response.text, 'html.parser')

    type_usd = mch.TYPE_USD
    type_eur = mch.TYPE_EUR

    usd_buy = soup.findAll('td', {'class': ["p-b-xs-2 p-y-1-sm"]})[4].get_text().strip()
    usd_sale = soup.findAll('td', {'class': ["p-b-xs-2 p-y-1-sm"]})[5].get_text().strip()

    last_rate = Rate.objects.filter(
        type=type_usd,
        source=source,
    ).order_by('created').last()

    if (
            last_rate is None or
            last_rate.sale != round_currency(usd_sale) or
            last_rate.buy != round_currency(usd_buy)
    ):
        Rate.objects.create(
            type=type_usd,
            sale=usd_sale,
            buy=usd_buy,
            source=source,
        )

    eur_buy = soup.findAll('td', {'class': ["p-b-xs-2 p-y-1-sm"]})[7].get_text().strip()
    eur_sale = soup.findAll('td', {'class': ["p-b-xs-2 p-y-1-sm"]})[8].get_text().strip()

    last_rate = Rate.objects.filter(
        type=type_eur,
        source=source,
    ).order_by('created').last()

    if (
            last_rate is None or
            last_rate.sale != round_currency(eur_sale) or
            last_rate.buy != round_currency(eur_buy)
    ):
        Rate.objects.create(
            type=type_eur,
            sale=eur_sale,
            buy=eur_buy,
            source=source,
        )
