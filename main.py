import telebot
from telebot import types
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TOKEN")

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
    username = str(callback.from_user.first_name)
    bot.edit_message_reply_markup(callback.message.chat.id, callback.message.id, reply_markup=None)
    if callback.data == 'accept':
        bot.send_message(callback.message.chat.id, "Accepted " + username)
    if callback.data == 'reject':
        bot.send_message(callback.message.chat.id, "Rejected " + username)


bot.infinity_polling()
