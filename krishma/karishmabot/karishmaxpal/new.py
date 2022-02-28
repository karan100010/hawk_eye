#the program takes a list as input
#The program will read the elements in this list by chunk, each comprised of 4 integers.
#In each chunk, the first element is the instruction, the second and the third elements are the input positions and the last element is the output position.
#The first element can only be of value 1 and 2. If the value is 1, the program will perform an addition (+), if the value is 2 the program will perform a multiplication (*).
#The program understands the second, third, and fourth values of each chunk as index numbers. It then looks into those index positions and takes
#the value from those positions as input. However, the fourth value is the position in which the output should be written.

def intcode(list):
    i = 0
    while i < len(list):
        if list[i] == 1:
            list[list[i+3]] = list[list[i+1]] + list[list[i+2]]
        elif list[i] == 2:
            list[list[i+3]] = list[list[i+1]] * list[list[i+2]]
        elif list[i] == 99:
            break
        i += 4
    return list

#the program takes a list as input
#The program will read the elements in this list by chunk, each comprised of 4 integers.
#In each chunk, the first element is the instruction, the second and the third elements are the input positions and the last element is the output position.
#The first element can only be of value 1 and 2. If the value is 1, the program will perform an addition (+), if the value is 2 the program will perform a multiplication (*).
#The program understands the second, third, and fourth values of each chunk as index numbers. It then looks into those index positions and takes
    #Assume that a pair of value at index 1 and 2 are missing. Let's call the missing value at these index positions as x and y. Find the value of x and y so
#that after feeding this list into the program written in question a), the result of the first element will be 4945036. You know that x and y will be
#somewhere between 1 and 99. Write this program in the function provided below.
import logging
from cv2 import FILE_NODE_UNIFORM
from numpy.lib.index_tricks import RClass
#from . import xpal
#from . import utils
import requests, json
from telegram.ext import (CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler, CallbackQueryHandler, CallbackContext)
from telegram import ReplyKeyboardMarkup, ParseMode, InlineKeyboardMarkup, InlineKeyboardButton, Update, ReplyKeyboardRemove
import pytesseract
from PIL import Image
import xetrapal
from xetrapal import telegramastras
import os
import feedgenerator


def find_missing_value(list,answer):
    for x in range(1,100):
        for y in range(1,100):
            list[1] = x
            list[2] = y
            if intcode(list)[0] == answer:
                return x,y


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
            return
        
        file_path = file_info.file_path
        logging.info("Downloading image {}".format(file_path))
        # try:

        #     context.bot.sendMessage(chat_id=update.message.chat_id,text="Downloading image {}".format(file_path))
        # except Exception as e:
        #     logger.error("{} {}".format(type(e), str(e)))
        #     return    
      #read image and convert into text using text extract

        
    
        try:
            text=pytesseract.image_to_string(Image.open(file_path),lang="hin+eng")
            logger.info("Downloading image {}".format(text))
        except Exception as e:
            logger.error("{} {}".format(type(e), str(e)))
            text=None
        
        only_text=[]
        for i in text:
            only_text.append(i[-1])
            
        text_string=" ".join(only_text)
        context.bot.sendMessage(chat_id=update.message.chat_id,text=text_string)
        context_dict={}
        #context_dict['sender']=update.message.from_user.username
        context_dict['text']=text_string
        logger.info(context_dict)
        dict_to_rssfeed(context_dict)
    

        
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