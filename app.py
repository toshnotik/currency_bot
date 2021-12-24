import requests
import json
import telebot


TOKEN = '5054117549:AAEXxyXJZowBLlrqu8DI6YJx0pp1MNHJKq4'

bot = telebot.TeleBot(TOKEN)

keys = {
    'евро': 'EUR',
    'доллар': 'USD',
    'рубль': 'RUB',
}

class ConvertionExeption(Exception):
    pass


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы узнать стоимость, введите команду в следующей форме:\n <коллическто переводимой валюты> <имя валюты> ' \
           '<в какую валюту перевести> ' \
           '\n Увидеть список доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n' .join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')

    if len(values) != 3:
        raise ConvertionExeption('Запрос введен не корректно.')

    amount, quote, base = values

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
    text = f'Цена {amount} {quote} в {base} - {total}'
    bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)