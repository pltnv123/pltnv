import telebot
from telebot import types
from config import keys, TOKEN
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

# Как делать кнопку
# conv_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)      one_time_keyboard=True - чтобы кнопки уползали, когда их не зовут
# buttons = []
# for val in keys.keys():
#     buttons.append(types.KeyboardButton(val.capitalize()))
# conv_markup.add(*buttons)
#
#Потом в     bot.send_message(message.chat.id, text, reply_markup = val)  добавили reply_markup = val) val - обхект

@bot.message_handler(commands=['start','help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате: \n <имя валюты>'\
'<в какую валюту перевести> ' \
'<количество переводимой валюты> \nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)
    # bot.send_message(message.chat.id, 'hello')

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text,)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) > 3:
            raise APIException('Слишком много параметров!')
        elif len(values) < 3:
            raise APIException('Слишком мало параметров!')
        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')
    except Exception as e:
        bot.send_message(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()