# -*- coding: utf8 -*-
import telebot
from telebot import types

bot = telebot.TeleBot('1178505929:AAEwS2trEjBsMuUyT_7BG0dxuz2MjcZ309o', threaded=False)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "Просто отправьте сообщение и оно появится на канале!")

@bot.message_handler(content_types=['text', 'photo'])
def answer(message):
    bot.forward_message('@buyaccountgame', message.chat.id, message.message_id)

while True:
    try:
        bot.polling(none_stop=True)
    except:
        print('Error')