import requests
import json
from config import keys

# Класс ошибок
class APIException(Exception):
    pass
#Класс проверки условия + возвращает значение total_base - (api конвертатор)
class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: int):
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}.')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}.')

        # r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        r = requests.get(f'https://v6.exchangerate-api.com/v6/aa74bfb66fad9e54480e348e/latest/{quote_ticker}')
        total_base = json.loads(r.content)["conversion_rates"][base_ticker]

        return total_base * amount