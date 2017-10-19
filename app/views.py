from app import app
import os
import telebot
from flask import request



bot = telebot.TeleBot('431904557:AAHrVTwCYRd_eaJggx7-_lfVmgGsODrR4N0')

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)


@app.route("/431904557:AAHrVTwCYRd_eaJggx7-_lfVmgGsODrR4N0", methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    URL_HOOK = "https://young-tundra-38775.herokuapp.com/431904557:AAHrVTwCYRd_eaJggx7-_lfVmgGsODrR4N0/"
    bot.set_webhook(url=URL_HOOK)
    return "!", 200

app.run(host="0.0.0.0", port=os.environ.get('PORT', 5000), debug = True)
"""
#Включить, если не работают веб хуки
bot.polling(none_stop=True)
"""
