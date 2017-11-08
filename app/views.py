# -*- coding: utf-8 -*-
from app import app
from app.config import token
from app.db_postgresql import SQL_Postgre
from app.csvEditor import csv_dict_reader
import os
import telebot
from flask import request
from app.timezone import get_utc_offset_timezone, get_time_from_another_timezone
import requests
import datetime
import time
import threading


bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Можно так
    # user = bot.get_me().__dict__['first_name']
    # Или так
    botName = bot.get_me().first_name # Берем имя бота
    userName = message.from_user.first_name # Берем имя пользователя
    chat_id = message.chat.id
    # Приветсвие
    bot.send_message(message.chat.id, userName + ", Приветствую! Меня зовут " + botName + ". Чем я могу помочь?" )
    list_commands = "Список команд: \n/time - Текущее время\n/contacts - Управление контактами"
    bot.send_message(message.chat.id, list_commands)


    '''
    Валидация клиента в системе
    '''

    # Получаем данные
    userId = message.from_user.id # id пользователя в telegram
    # Являетеся ли ботом? В документации есть is_bot
    firstName = message.from_user.first_name # Имя пользователя
    userName = message.from_user.username # Имя, отображающееся в telegram
    lastName = message.from_user.last_name # Фамилия пользователя
    languageCode = message.from_user.language_code # Используемый язык
    msg_date = message.date #Дата отправки /start
    curr_utc_time = datetime.datetime.utcnow()
    timezone = get_utc_offset_timezone(msg_date)

    db = SQL_Postgre()
    # check_user_availible = True - Пользователь существует в системе
    #                      = False - Пользователь не существует в системе
    check_user_availible = db.check_user_id(userId)
    if check_user_availible == False:
        a = db.new_user(userId,firstName,userName,lastName,timezone)

    db.close()

@bot.message_handler(commands=['time'])
def send_time_now(message):
    bot.send_message(message.chat.id, 'Доброе утро, сегодня {dt:%A} {dt:%B} {dt.day}, {dt.year},{dt.hour},{dt.minute}: '.format(dt = datetime.datetime.utcnow()))

@bot.message_handler(commands=['contacts'])
def send_welcome_contacts(message):
    bot.send_message(message.chat.id, "Список команд:\n /createContact - Загрузить контакты файлом")

@bot.message_handler(func=lambda message: True, commands=['createContact'])
def new_contact_list(message):
    bot.send_message(message.chat.id, 'Пожалуйста, загрузите файл в формате GOOGLE CSV\nПодробнее: https://www.google.com/contacts/u/0/?cplus=0#contacts\nЕще->Экспорт->Выберите формат файла для экспорта->\
                                       Google CSV (для импорта в аккаунт Google)')

# Загрузка документа
@bot.message_handler(content_types=['document'])
def downloadFile(message):
    userId = message.from_user.id
    a = message.document.file_id
    file_info = bot.get_file(a)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))
    csv_dict_reader(file.text, userId)
    bot.send_message(message.chat.id, "Файл успешно загружен.")

#from app import contact_timer
'''
def start_runner():
    thread = threading.Thread(target=run_job)
    thread.start()

def run_job():
    while True:
        now = datetime.now()
        print(now.year)
        print(now.month)
        print(now.day)
        print(now.minute)
        print(now.second)
        time.sleep(3)
        db = SQL_Postgre()
        contact_info = db.find_data_contact(now.month,now.day)
        if contact_info.__len__() != 0:
            print(contact_info[0][0])
            strmsg = 'День рождение у' + str(contact_info[0][1]) + ' ' + str(contact_info[0][0])
            bot.send_message(contact_info[0][2], strmsg)
        db.close()
'''

def start_contact_notification():
    thread = threading.Thread(target=run_thread)
    thread.start()

def run_thread():
    global day_today
    day_today = 0
    while True:
        current_date = datetime.date.today()    # Узнаем текущую дату
        current_time = datetime.datetime.now()

        for utc in range(-12,12):
            if datetime.datetime.now().hour + utc == 13 and datetime.datetime.now().minute == 0 :  # Уведомление пока настроено статически на 9 утра (Но если загрузим на серевер, то он будет будет присылать в 9 утра по времени сервера)
                db = SQL_Postgre()
                data_contact_withTimeZone = db.get_user_timezone(utc)
                for currData in data_contact_withTimeZone:
                    data_contact = db.find_data_contact(current_date.month, current_date.day, currData[0])
                    if len(data_contact) != 0:
                        for row in data_contact:
                            bot.send_message(row[2], str(row[0]))
                db.close()
            '''
            if datetime.datetime.now().hour == 9:  # Уведомление пока настроено статически на 9 утра (Но если загрузим на серевер, то он будет будет присылать в 9 утра по времени сервера)
                day_today = current_date.day
                db = SQL_Postgre()
                data_contact = db.find_data_contact(current_date.month, current_date.day)
                if len(data_contact) != 0:
                    for row in data_contact:
                    
                        bot.send_message(row[2], str(row[0]))
                db.close()
            '''
        time.sleep(60)


# Запускаем новый поток, который каждый день смотрит кому нужно отправить уведомления из БД контактов
start_contact_notification()



#!------------------------------------------------------------------------------------------!#
# СЕРВЕРНАЯ ЧАСТЬ (НЕ ТРОГАТЬ)
#!------------------------------------------------------------------------------------------!#
"""
@app.route('/' + token, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "POST", 200


@app.route("/")
def web_hook():
    bot.remove_webhook()
    bot.set_webhook(url='https://miass-bot.herokuapp.com/' + token)
    return "CONNECTED", 200
"""
#app.run(host="0.0.0.0", port=os.environ.get('PORT', 5000)) - это нам не нужно, потому что мы выполняем команду: gunicorn runp-heroku:app

# Если web-хуки не работают или хочешь запустить на локальной машине
# Необходимо закомментировтаь серверную часть и включить bot.polling

#Включить, если не работают веб хуки

#Если появляется ошибка "Conflict: can\'t use getUpdates method while webhook is active", меняем токен бота
# Пишем @botFather
# /revoke
#
# /MiassSuperBot

# или
# heroku ps:scale web=0 #! Отключаем сервер
# Телеграма отработает хуки
# heroku ps:scale web=1 #! Включаем сервер


#или выполняем bot.remove_webhook()
bot.remove_webhook()
bot.polling(none_stop=True)


