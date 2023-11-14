import telebot
from telebot import types
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TOKEN")

bot = telebot.TeleBot(token)


@bot.message_handler()
def monitor_chat(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Approve", callback_data='approve')
    button2 = types.InlineKeyboardButton("Reject", callback_data='reject')
    markup.add(button1, button2)
    if "#summary" in message.text:
        msg = bot.send_message(message.chat.id,
                               "Resolution:" + message.text.replace('#summary', ''),
                               reply_markup=markup)
        send_json(msg, True)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    username = str(callback.from_user.first_name)
    bot.edit_message_reply_markup(callback.message.chat.id, callback.message.id, reply_markup=None)
    if callback.data == 'approve':
        bot.send_message(callback.message.chat.id,
                         "The resolution was approved")
        send_json(callback.message, True)
    if callback.data == 'reject':
        bot.send_message(callback.message.chat.id,
                         "Please correct the resolution in accordance with the partner's request")
        send_json(callback.message, False)


def send_json(message, status):
    json = {
        "resolution": message.text.replace('Resolution:', ''),
        "chat_id": message.chat.id,
        "message_id": message.id,
        "status": status
    }
    bot.send_message(message.chat.id, str(json))

bot.infinity_polling()
