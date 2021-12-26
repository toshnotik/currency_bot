import telebot
from config import keys, TOKEN
from utilits import ConvertionExeption, CurrencyConvert

bot = telebot.TeleBot(TOKEN)

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
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionExeption('Запрос введен не корректно.')

        amount, quote, base = values
        total = CurrencyConvert.convert(quote, base, amount)
    except ConvertionExeption as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} = {total}'
        bot.send_message(message.chat.id, text)



bot.polling(none_stop=True)