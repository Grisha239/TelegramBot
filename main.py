import telebot
from telebot import types
import os
from dotenv import load_dotenv
import requests

load_dotenv()
token = os.getenv("TOKEN")
url = os.getenv("URL")
bot = telebot.TeleBot(token)


@bot.message_handler()
def monitor_chat(message):
    if '#summary' in message.text and '#summary' != message.text:
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Approve", callback_data='approve')
        button2 = types.InlineKeyboardButton("Reject", callback_data='reject')
        markup.add(button1, button2)
        msg = bot.send_message(message.chat.id,
                               "🚕 Resolution of the meeting:" + message.text.replace('#summary', ''),
                               reply_markup=markup)
        send_json(msg, True)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    username = str(callback.from_user.first_name)
    bot.edit_message_reply_markup(callback.message.chat.id, callback.message.id, reply_markup=None)
    if callback.data == 'approve':
        bot.edit_message_text(chat_id=callback.message.chat.id,
                              message_id=callback.message.id,
                              text=callback.message.text + "\n\n✅ The resolution was approved")
        bot.send_message(callback.message.chat.id,
                         "✅ The resolution was approved")
    if callback.data == 'reject':
        send_json(callback.message, False)
        bot.edit_message_text(chat_id=callback.message.chat.id,
                              message_id=callback.message.id,
                              text=f"{callback.message.text}\n\n⛔️ Please correct the resolution in accordance with the partner's request")
        bot.send_message(callback.message.chat.id,
                         "⛔️ Please correct the resolution in accordance with the partner's request")


def send_json(message, status):
    json = {
        "resolution": f"{message.text.replace("🚕 Resolution of the meeting:", '')}",
        "chat_id": message.chat.id,
        "message_id": message.id,
        "status": status
    }
    requests.post(url, json)


if __name__ == "__main__":
    bot.polling()
