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


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы узнать стоимость, введите команду в следующей форме:\n <имя валюты> ' \
           '<в какую валюту перевести> ' \
           '<коллическто переводимой валюты>\n Увидеть список доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n' .join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    quote, base, amount = message.text.split(' ')
    r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={keys[quote]}&tsyms={keys[base]}')
    total_base = json.loads(r.content)[keys[base]]
    total = total_base * float(amount)
    text = f'Цена {amount} {quote} в {base} - {total}'
    bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)