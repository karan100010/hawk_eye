# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
# from karishmatgbot.xpal import *
import logging
from re import I
from cv2 import FILE_NODE_UNIFORM
from numpy.lib.index_tricks import RClass
from . import xpal
from . import utils
import requests, json

import feedgenerator
import pytesseract
from PIL import Image


# from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
#                          ConversationHandler)
from telegram.ext import (CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler, CallbackQueryHandler, CallbackContext)
from telegram import ReplyKeyboardMarkup, ParseMode, InlineKeyboardMarkup, InlineKeyboardButton, Update, ReplyKeyboardRemove
import xetrapal
from xetrapal import telegramastras
import os
verbose=True
#import sys

#sys.path.append("/opt/xetrapal")


memberbotconfig = xetrapal.karma.load_config(configfile="/opt/karishmabot-appdata/karishmatgbot.conf")
karishmatgbot = xetrapal.telegramastras.XetrapalTelegramBot(config=memberbotconfig, logger=xpal.karishmatgbotxpal.logger)
logger = karishmatgbot.logger
GETMOBILE, PROCESS_MESSAGE = range(2)

send_contact_text = u'\U0001F4CD Send Contact'

loop_text = u'\U0001F960 Loop'
exit_text = u'\U0001F44B Bye'
#contact_keyboard = [
#                    [{'text': send_contact_text, 'request_contact': True}]
#                    ]
#member_base_keyboard = [
#                        [exit_text]
#                        ]

main_menu_header_text = '''\
    Hi! My name is Zhu Li.\n
'''

def facts_to_str(user_data):
    facts = list()
    logger.info("Converting facts to string")
    for key, value in user_data.items():
        facts.append(u'{} - {}'.format(key, repr(value)))
    logger.info("Converted facts to string")
    return "\n".join(facts).join(['\n', '\n'])

def get_rasa_response(username,message_text,hostname="http://localhost"):
    logger.info("Trying")
    resturl=":5005/webhooks/rest/webhook"
    jsondata={}
    jsondata['sender']=username
    jsondata['message']=message_text
    response=requests.post(hostname+resturl,json=jsondata)
    return response.json()

def get_karishma_response(username,message_text,hostname="http://localhost"):
    resturl=":5000/listener"
    jsondata={}
    jsondata['sender']=username
    jsondata['text']=message_text
    logger.info("Trying",jsondata)
    response=requests.post(hostname+resturl,json=jsondata)
    return response.json()


def main_menu(update: Update, context: CallbackContext):
    logger.info(context.user_data)
    user_data = context.user_data
    try:
        #user_data['member'] = xpal.get_member_by_tgid(update.message.from_user.id)
        user_data['member'] = xpal.get_member_by_username(update.message.from_user.username)
        logger.info(u"{}".format(user_data))
        if user_data['member'] is None:
            update.message.reply_text("Sorry, this service is for whitelisted members only.")
            #return ConversationHandler.END
            return GETMOBILE
        logger.info("Main Menu presented to member {}".format(user_data['member'].username))
        update.message.reply_text(main_menu_header_text,  parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardRemove())
        return PROCESS_MESSAGE
    except Exception as e:
        logger.error("{} {}".format(type(e), str(e)))


def loop(update: Update, context: CallbackContext):
    logger.info(context.user_data)
    logger.info(update.message.text)
    # if upadte cotains image download image 
    if update.message.photo or update.message.document:
        logger.info("Downloading image")
        logger.info(update.message.photo)
        file_id = update.message.photo[-1].file_id
        # logger.info("Downloading image {}".format(file_id))
        # bot has no attribute get_file
        try:
            file_info = context.bot.get_file(file_id)
        except Exception as e:
            logger.error("{} {}".format(type(e), str(e)))


        
        file_path = file_info.file_path
        logging.info("Downloading image {}".format(file_path))
        # try:

        #     context.bot.sendMessage(chat_id=update.message.chat_id,text="Downloading image {}".format(file_path))
        # except Exception as e:
        #     logger.error("{} {}".format(type(e), str(e)))
        #     return    
    
        logger.info("Downloading image {}".format(file_info))
        #download image to local file
        download=context.bot.get_file(file_id)
        #save the file as image.jpg in current directory
        download.download('image.jpg')


        
        try:
            text=pytesseract.image_to_string(Image.open("image.jpg"),lang="hin")
            #add utf-8 encoding to text
          
            logger.info("Downloading image {}".format(text))
        except Exception as e:
            logger.error("{} {}".format(type(e), str(e)))
            text=None
        
        #write text to a file and setnd the file

        #remove image from local directory
        os.remove("image.jpg")    
       # text_string=" ".join(only_text)
        context.bot.sendMessage(chat_id=update.message.chat_id,text=text)
      
        #context_dict['sender']=update.message.from_user.username
  

        
    if update.message.text=="/bye":
        return exit(update,context)
    #text = os.popen("fortune").read()
    logger.info("{} {}".format(context.user_data['member'].username,update.message.text))
    text=get_karishma_response(username=context.user_data['member'].username, message_text=update.message.text)
    logger.info(str(text))
    if verbose:
        update.message.reply_text(str(text), parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardRemove())
    return PROCESS_MESSAGE

#write a program to turn a json object into a rssfeed
def dict_to_rssfeed(json_object):
    rssfeed=feedgenerator.Rss201rev2Feed(title="Xetrapal RSS Feed", link="http://www.xetrapal.com", description="Xetrapal RSS Feed")
    rssfeed.add_item(title=json_object['text'], link="http://www.xetrapal.com", description=json_object['text'])
    try:
   #append if file exists write if file does not exist
      
        with open('test.rss', 'w') as fp:
            rssfeed.write(fp, 'utf-8')
    except Exception as e:
        logger.info("{} {}".format(type(e), str(e)))
def add_todo(update: Update, context: CallbackContext):
    logger.info(context.user_data)
    if update.message.text=="/bye":
        return exit(update,context)
    #text = os.popen("fortune").read()
    logger.info("{} {}".format(context.user_data['member'].username,update.message.text))
    text=get_rasa_response(username=context.user_data['member'].username, message_text=update.message.text,hostname="http://192.168.56.1")
    update.message.reply_text(update.message.text.replace("TODO:","Added TODO - " ), parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardRemove())
    return PROCESS_MESSAGE

def add_txn(update: Update, context: CallbackContext):
    logger.info(context.user_data)
    if update.message.text=="/bye":
        return exit(update,context)
    #text = os.popen("fortune").read()
    logger.info("{} {}".format(context.user_data['member'].username,update.message.text))
    text=get_rasa_response(username=context.user_data['member'].username, message_text=update.message.text,hostname="http://192.168.56.1")
    update.message.reply_text(update.message.text.replace("TXN:","Added TXN - " ), parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardRemove())
    return PROCESS_MESSAGE

def add_rel(update: Update, context: CallbackContext):
    logger.info(context.user_data)
    if update.message.text=="/bye":
        return exit(update,context)
    #text = os.popen("fortune").read()
    logger.info("{} {}".format(context.user_data['member'].username,update.message.text))
    text=get_rasa_response(username=context.user_data['member'].username, message_text=update.message.text,hostname="http://192.168.56.1")
    update.message.reply_text(update.message.text.replace("REL:","Added relationship - " ), parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardRemove())
    return PROCESS_MESSAGE

def set_mobile(update: Update, context: CallbackContext):
    logger.info(u"{}".format(update.message.contact))
    member = xpal.get_member_by_mobile(update.message.contact.phone_number.lstrip("+"))
    if member:
        member.tgid = update.message.contact.user_id
        member.save()
        user_data['member'] = member
        logger.info("Main Menu presented to member {}".format(user_data['member'].username))
        markup = ReplyKeyboardMarkup(member_base_keyboard, one_time_keyboard=True)
        update.message.reply_text(main_menu_header_text, reply_markup=markup, parse_mode=ParseMode.HTML)
        return PROCESS_MESSAGE
    else:
        update.message.reply_text("Sorry, you don't seem to be listed!")
        return ConversationHandler.END


def cancel(bot, update, user_data):
    logger.info(u"Cancelling Update {}".format(user_data))
    markup = ReplyKeyboardMarkup(member_base_keyboard, one_time_keyboard=True)
    update.message.reply_text(u'Cancelled!', reply_markup=markup)
    return PROCESS_MESSAGE


def exit(update: Update, context: CallbackContext):
    update.message.reply_text("Bye!")
    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


# function to check if telegram.Message object contains an image
def is_image(message):
    logger.info(message.content_type)
    return message.content_type == 'photo' or message.content_type == 'document'


states={
    GETMOBILE: [MessageHandler(Filters.text,
                               exit,
                               pass_user_data=True),
                MessageHandler(Filters.contact,
                               set_mobile,
                               pass_user_data=True),
                ],
    PROCESS_MESSAGE: [
                    MessageHandler(Filters.regex('^(TODO:)'), add_todo, pass_user_data=True),
                    MessageHandler(Filters.regex('^(TXN:)'), add_txn, pass_user_data=True),
                    MessageHandler(Filters.regex('^(REL:)'), add_rel, pass_user_data=True),
                    MessageHandler(Filters.all, loop, pass_user_data=True),
            
                    #CallbackQueryHandler(open_xchange_button, pass_user_data=True),
                  ],

}


def setup():
    # Create the Updater and pass it your bot's token.
    updater = karishmatgbot.updater
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', main_menu)],
        states=states,
        fallbacks=[]#[RegexHandler('^[dD]one$', exit, pass_user_data=True)]
    )
    dp.add_handler(conv_handler)
    # log all errors
    dp.add_error_handler(error)
    # Start the Bot
    # updater.start_polling()
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    # updater.idle()


def single_update():
    p = karishmatgbot.get_latest_updates()
    for update in p:
        karishmatgbot.updater.dispatcher.process_update(update)
    return p


if __name__ == '__main__':
    setup()
    karishmatgbot.updater.start_polling()
    karishmatgbot.updater.idle()
