# -*- coding: utf8 -*-
import telebot
from telebot import types
from datetime import datetime
import pymysql

bot = telebot.TeleBot('1178505929:AAEwS2trEjBsMuUyT_7BG0dxuz2MjcZ309o', threaded=False)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "Просто отправьте сообщение и оно появится на канале!")

@bot.message_handler(commands=['donate'])
def money(message):
    bot.send_message(message.chat.id, "За платной подпиской обращайтесь к @Odmen_228")

@bot.message_handler(content_types=['text', 'photo'])
def answer(message):
    chat_id = message.chat.id
    now = datetime.today()
    
    con = pymysql.connect('eu-cdbr-west-03.cleardb.net', 'ba181f0e44fd71', '322a1c67', 'heroku_babf1d4d975c9ec')
    with con:
        cur = con.cursor()

        cur.execute("SELECT * FROM members WHERE chat_id = %s", (chat_id,))
        row = cur.fetchall()
        
        if len(row) == 0:
            cur.execute("INSERT INTO members (chat_id, date, sub, sub_date) VALUES (%s, %s, %s, %s)", (chat_id, now, 0, now))
            bot.forward_message('@buyaccountgame', chat_id, message.message_id)
        else:
            cur.execute("SELECT date FROM members WHERE chat_id = %s", (chat_id,))
            now2 = cur.fetchall()
            now2 = now2[0][0] 
            
            delta = now - now2
            seconds = delta.seconds
            minutes = seconds // 60

            cur.execute("SELECT sub FROM members WHERE chat_id = %s", (chat_id,))
            sub = cur.fetchall()
            sub = sub[0][0]

            if int(sub) == 1:
                cur.execute("SELECT sub_date FROM members WHERE chat_id = %s", (chat_id,))
                now_don = cur.fetchall()
                now_don = now_don[0][0]

                delta_don = now - now_don
                seconds_don = delta_don.seconds
                days = seconds_don // 86400
                if days < 30:
                    if minutes >= 10:
                        bot.forward_message('@buyaccountgame', chat_id, message.message_id)
                        cur.execute("UPDATE members SET date = %s WHERE chat_id = %s", (now, chat_id))
                    else:
                        bot.send_message(chat_id, 'Для отправки сообщения подождите ещё ' + str(10 - minutes) + 'минут')
                else:
                    bot.send_message(chat_id, 'Ваша подписка закончилась((( Приобретите её снова командой\n/donate')
                    cur.execute("UPDATE members SET sub = %s WHERE chat_id = %s", (0, chat_id))
            else:
                hours = seconds // 3600
                if hours >= 1:
                    bot.forward_message('@buyaccountgame', chat_id, message.message_id)
                    cur.execute("UPDATE members SET date = %s WHERE chat_id = %s", (now, chat_id))
                else:
                    bot.send_message(chat_id, 'Для отправки сообщения подождите ещё ' + str(60 - minutes) + 'минут')
                    bot.send_message(chat_id, 'Для снятия ограничений на отправку приобретите премиум версию командой \n/donate')

        cur.close()

while True:
    try:
        bot.polling(none_stop=True)
    except:
        print('Error')
