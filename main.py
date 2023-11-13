import telebot
from telebot import types

token = "6483024611:AAFbrhUQETUEQJB2K5pwAmr8j8qUJ3bhZ7Y"

bot = telebot.TeleBot(token)


@bot.message_handler()
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Принять", callback_data='accept')
    button2 = types.InlineKeyboardButton("Отклонить", callback_data='reject')
    markup.add(button1, button2)
    if "#summary" in message.text:
        msg = bot.send_message(message.chat.id,
                               "Resolution text: " + message.text.replace('#summary', ''),
                               reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'accept':
        bot.send_message(callback.message.chat.id, "Accepted")
    if callback.data == 'reject':
        bot.send_message(callback.message.chat.id, "Rejected")


bot.infinity_polling()
