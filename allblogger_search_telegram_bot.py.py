#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  allblogger_search_telegram_bot.py.py
#
# Requires :
#    pyTelegramBotAPI
#    BeautifulSoup
#
import telebot
from bs4 import BeautifulSoup
import urllib

# Change Here
########################################################################
default_max_results  = 30
agent                = "Mozilla/5.0"
telegram_token       = ""
not_found_msg        = "Not Found"

help_msg = """Welcome To Blogger Telegram Bot Search.
/search <blog name> <search for>
  example : /search arfedora dnf

/help
"""
########################################################################


bot = telebot.TeleBot(telegram_token)


def blogger_search(blog_name,search):
    result  = ""
    try:
        web = "https://{}.blogspot.com".format(blog_name)
        url = urllib.request.Request("{}/search?{}&{}".format(web,urllib.parse.urlencode({"q":search}),urllib.parse.urlencode({"max-results":str(default_max_results)})),headers={"User-Agent":agent})
        opurl = urllib.request.urlopen(url)
        soup = BeautifulSoup(opurl,"html.parser")
        for h2 in soup.findAll("h2",{"class":"post-title entry-title"}):
            result += h2.a.text
            result += h2.a.get("href")
            result += "\n"
    except Exception as e:
        result = str(e)
    if len(result)==0:
        if len(not_found_msg)==0:
            result = "Not Found"
        else:
            result = not_found_msg
    return result


    
@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, help_msg)

@bot.message_handler(commands=['search'])
def send_search_result(message):
    msg  = message.text.strip().split()
    text = "Enter Blog Name And what you want to search for after '/search'"
    if len(msg)<3:
        bot.reply_to(message,text )
    else:
        text = blogger_search(msg[1],msg[2])
        bot.reply_to(message, text)

bot.polling()
