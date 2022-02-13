import googletrans
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from newspaper import Article
import requests
from datetime import datetime
import pandas 
from googletrans import Translator
import re
import logging
from stanza.research.nlp.core.doc import Document
# add logging to the file using dd-mm-yyyy:tt also inluding the line number of the info format
###logger=logging.basicConfig(filename='logs/logs.log',level=logging.INFO,format='%(asctime)s:%(lineno)d:%(levelname)s:%(message)s')
#given a pandas dataframe,column name and a string find that string in the column and return datafreme where the string is found in the column and reset the index of the new dataframe

def find_string(df,column,string):
    df_new=df[df[column].str.contains(string)]
    df_new=df_new.reset_index(drop=True)
    return df_new

# deduct language of a text using googletrans packege
def language_detect(text):
    translator = Translator()
    return translator.detect(text).lang

#get total number of words in a text

def total_words(text):
    return len(text.split())

# extact quotes from a text

def extect_quotes(text):
    quotes=[]
    for i in text.split():
        if i.startswith('"') and i.endswith('"'):
            quotes.append(i)
    return quotes
#clean words that start with non alphabet characters
def clean_words(text):
    text=text.lower()
    text=re.sub('[^a-zA-Z0-9]+', ' ', text)
    return text
#word count of each word in text

def word_count(text):
    word_count={}
    for i in text.split():
        if i in word_count:
            word_count[i]+=1
        else:
            word_count[i]=1
    return word_count        

#extract sentences from a text
#return a list of sentences

def ext_sentence(text):
    sentences=[]
    for i in text.split():
        if i.endswith('.'):
            sentences.append(i)
    return sentences

#find similer senternce in a text
# return a dictionary of similar sentences where the key and value are the sentence and the similarity score
#write a fuction that takes two sentence and calulate the cosine similarity between them using word to vec and return the similarity score
def sentence_similarity(sen1,sen2):
    sen1=clean_words(sen1)
    sen2=clean_words(sen2)
    sen1_word_count=word_count(sen1)
    sen2_word_count=word_count(sen2)
    common_words=list(set(sen1_word_count.keys()).intersection(set(sen2_word_count.keys())))
    sum_of_sen1=0
    sum_of_sen2=0
    for i in common_words:
        sum_of_sen1+=sen1_word_count[i]*sen1_word_count[i]
        sum_of_sen2+=sen2_word_count[i]*sen2_word_count[i]
    sum_of_sen1=sum_of_sen1**(1/2)
    sum_of_sen2=sum_of_sen2**(1/2)
    sum_of_sen1_sen2=0
    for i in common_words:
        sum_of_sen1_sen2+=sen1_word_count[i]*sen2_word_count[i]
    return sum_of_sen1_sen2/(sum_of_sen1*sum_of_sen2)


def find_similar_sentence(text,sentence):
    sentences=ext_sentence(text)
    similar_sentence={}
    for i in sentences:
        similar_sentence[i]=sentence_similarity(i,sentence)
    return similar_sentence
#use stanza library to extract part of speech from a text
#return a dictionary of words and their part of speech

def get_pos(text):
    
    doc=Document(text)
    doc.sentences[0].parse()
    pos_dict={}
    for i in doc.sentences[0].words:
        pos_dict[i.text]=i.pos
    return pos_dict


   