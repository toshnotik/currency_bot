import requests
import json
from config import keys


class ConvertionExeption(Exception):
    pass


class CurrencyConvert:
    @staticmethod
    def convert(quote: str, base: str, amount: str):

        if quote == base:
            raise ConvertionExeption(f'Вы ввели одинаковую валюту.')

        try:
            quote_tiker = keys[quote]
        except KeyError:
            raise ConvertionExeption(f'Не удалось обработать валюту {quote}')

        try:
            base_tiker = keys[base]
        except KeyError:
            raise ConvertionExeption(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionExeption(f'Не удалось обработать колличество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_tiker}&tsyms={base_tiker}')
        total_base = json.loads(r.content)[keys[base]]
        total = total_base * float(amount)

        return round(total, 2)