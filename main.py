import telebot
import os
import requests
import json
from telebot import types
from dotenv import load_dotenv
from urllib.request import urlopen

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
    userid = callback.from_user.id
    response_url = (os.getenv("RESPONSE_URL") + str(userid))
    response = urlopen(response_url)
    data_json = json.loads(response.read())
    if not data_json["IsInBlacklist"]:
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
    message_text = message.text.replace('🚕 Resolution of the meeting:', '').replace('\n', '\\n').replace('\t', '\\t')
    hook_info = {
        "resolution": f"{message_text}",
        "chat_id": message.chat.id,
        "message_id": message.id,
        "status": status
    }
    requests.post(url, hook_info)


if __name__ == "__main__":
    bot.polling()
