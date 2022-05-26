#write a fuction that takes google sheets as input and returns a json object

from asyncio.log import logger
from distutils.log import error
from fnmatch import translate
from msilib import add_data
from matplotlib.pyplot import text, title
from regex import D
from sqlalchemy import create_engine
import gspread
from matplotlib import image
from oauth2client.service_account import ServiceAccountCredentials
from newspaper import Article
import requests
from datetime import datetime, timedelta
import pandas 
from bs4 import BeautifulSoup
import re,os
from googletrans import Translator
from collections import Counter
import stanza
from urllib3 import Retry
from text_based_func import *
from datetime import datetime
from time import sleep
import configparser
from geopy.geocoders import Nominatim
from langdetect import detect
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
#configure logger to print to file and console


from logs import *
rootLogger.info("Starting the program") 

def read_google_sheet_to_json(sheet):
   
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name( secret_key,scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet).sheet1
    data = sheet.get_all_records()
    return data


 # given a link scrape the news,title,date_published artical using the newspaper3k library and return a json object

def news_scraper(link,retries=3,timeout=10):
    for i in range(retries):
        try:
            article = Article(link) 
            break

        except:
            rootLogger.error("Error in scraping article from link {}".format(link))
            rootLogger.info("Retrying in 5 sconds this is retry number {}".format(i+1))
            sleep(timeout)
             
            
    if article:
        for i in range(retries):    
            try:
                article.download()
                        
                article.parse()
                article.nlp()
                data = {
                    'html': article.html,
                    'title': article.title,
                    'link': link,
                    'date': article.publish_date,
                    'text': article.text,
                    "summary": article.summary,
                "date_scraped": datetime.now()  }
                return data

            except:
                rootLogger.error("Error in downloading article from link {}".format(link))
                rootLogger.info("Retrying in 5 sconds this is retry number {}".format(i+1))

                sleep(timeout)
                continue    
 # if article is not downloaded then return {}
    if not article.text:
        #write the link to a file called failed_links.txt if file aleready exits if not create a new file
        with open("failed_links.txt","a+") as f:
            f.write(link+"\n")         
        return {"error":"artical not found"}  
        
    
          
    

 #create a postgresql table 


#create a fuction that takes a list of json objects ,name of the table and user and inserts them into a postgresql table three parameters link,title,text


#search a term with google search api in python
#restrict the serch to only the past week
def search(term,cx,api_key,days=7,start_index=0):        
    search_url = "https://www.googleapis.com/customsearch/v1?key={}&cx={}&q={}&start={}&dateRestrict=d{}".format(api_key,cx,term,start_index,days)
    response = requests.get(search_url)
    return response.json()

def get_links(term,cx,api_key):
    page_index=0
    all_links=[]
    while True:
        search_url = "https://www.googleapis.com/customsearch/v1?key={}&cx={}&q={}&start={}".format(api_key,cx,term,page_index)
        response = requests.get(search_url)
        json_response = response.json()
        try:
            links=[i['link'] for i in json_response['items']]
        except:
            #logger.info("Error in getting links")
            return all_links    
        all_links=all_links+links
        #logger.info(len(all_links))
        if len(links)<10:
            #logger.info("done")
            break
        else:
            page_index+=10
            
    return all_links


#converting a dataframe with columns links, discription ,text ,title to a dataframe with columns links, discription ,text ,title, theme
# into a rss stream
def to_rss(df):
    rss_stream=[]
    for i in df.index:
        rss_stream.append({"link":df.loc[i,"link"],"description":df.loc[i,"description"],"text":df.loc[i,"text"],"title":df.loc[i,"title"],"theme":df.loc[i,"theme"]})
    return rss_stream
# extrct date and time form the following format'2022-02-10T23:17:52+05:30' use the bit after + as time zone return the time with adding the time zone

def date_time_extract(date_time):
    
    date_time=date_time.split("+")
    date_time=date_time[0]
    date_time=date_time.split("T")
    date=date_time[0]
    time=date_time[1]
    date=date.split("-")
    time=time.split(":")
    date=datetime(int(date[0]),int(date[1]),int(date[2]),int(time[0]),int(time[1]),int(time[2]))
    return date 
translator=Translator()    

# read cx,keyword,days=30,start_index,theme_dict form a config file using config parser
def get_full_data(keyword,conf_file,theme_dict,start_index=0,days=30):

    config = configparser.ConfigParser()
    config.read(conf_file)
    cx=config['Arguments']['cx']
    loc = Nominatim(user_agent="GetLoc")
   
    api_key=config['Arguments']['api_key'].split(",")
    #theme_dict=config['Arguments']['theme_dict']
    api_key_current=api_key[0]
    #find the index of api_key_current in api_key
    rootLogger.info("Api key set to {}".format(api_key_current))
    index=api_key.index(api_key_current)

    data=[]
    rootLogger.info("getting links")

    while True: 
        search_result=search(keyword,cx=cx,days=days,start_index=start_index,api_key=api_key_current)
        rootLogger.info("getting links form search result {}".format(search_result))
      
        rootLogger.info("start index {}".format(start_index))
         #look for key error in search result if error in search reusult return data list with serach result
        if "error" in search_result:
           
                          
            if  search_result["error"]["code"] == 429:
                rootLogger.info("Error 429")
                for i in api_key[index:]:
                    search_result=search(keyword,cx=cx,days=days,start_index=start_index,api_key=api_key_current)
                    rootLogger.info("getting links form search result {}".format(search_result))
                    

                    if "error" in search_result and search_result["error"]["code"] == 429:
                        if api_key_current !=api_key[-1]:
                            index+=1
                            api_key_current=api_key[index]
                            rootLogger.info("changed api key to {} index is {}".format(api_key_current,index))
                            rootLogger.info(search_result)
                        else:    
                            rootLogger.error("Error in search result {}".format(search_result))
                            data.append(search_result)
                            return data
                             
                    else:
                        rootLogger.info("Serach is working well with the new api key {}".format(api_key_current))
                        break


                    
        
  #incriment the start index by 10 each time till you get less than 10 links
        if "searchInformation" not in search_result:
            return search_result


        
        if int(search_result["searchInformation"]["totalResults"])>0:
            data.append({"status":"success","results":search_result["searchInformation"]["totalResults"],"start_index":search_result["queries"]["request"][0]["startIndex"],"search_term":keyword})
            for i in search_result['items']:
                
                all_data={}
                all_data["state"]="Uttar Pradesh"
                try:
                    if "og:site_name" in i["pagemap"]["metatags"][0]:
                        all_data["publication"]=i["pagemap"]["metatags"][0]["og:site_name"]
                        rootLogger.info("publication {}".format(all_data["publication"]))
                    else:
                        all_data["publication"]=i['displayLink'].split(".")[1]  
                        rootLogger.info("publication {}".format(all_data["publication"]))   
                except:
                    all_data["publication"]="Unknown"
                    rootLogger.info("publication {}".format(all_data["publication"]))
               

                try:
                    all_data["link"]=i["link"]
                    rootLogger.info("link {}".format(all_data["link"]))
                except:
                    all_data["link"]="Unknown"
                    rootLogger.info("link {}".format(all_data["link"]))
                if all_data["publication"]=="Navbharat Times":
                    all_data["location"]=all_data["link"].split("/")[5]
                    rootLogger.info("location {}".format(all_data["location"]))
                else:
                    all_data["location"]=all_data["link"].split("/")[4].split("-")[0]
                    rootLogger.info("location {}".format(all_data["location"]))
#                try to get location coordinates from the location name
                
                
                if all_data["link"]!="Unknown":
                    news=news_scraper(all_data["link"])
                    #if error in news return all_data with error and continue
                    

                    if "title" in news:
                        all_data["title"]=news["title"]
                        rootLogger.info("title {}".format(all_data["title"]))
                        
                    else:
                        all_data["title"]="Unknown"
                        rootLogger.info("title {}".format(all_data["title"]))
                     
                else:
                    all_data["title"]="Unknown"
                    rootLogger.info("title {}".format(all_data["title"]))
                if "error" in news:
                        all_data["error"]=news["error"]
                        rootLogger.info("error {}".format(all_data["error"]))
                        data.append(all_data)
                        break
                
                try:
                    all_data["text"]=news["text"]
                    rootLogger.info("text {}".format(all_data["text"]))
                except:
                    all_data["text"]="Unknown"
                    rootLogger.info("text {}".format(all_data["text"]))
                
                try:
                    all_data["char_count"]=len(news["text"])           
                except:
                    all_data["char_count"]="Unknown"
                    rootLogger.info("char_count {}".format(all_data["char_count"]))  

#                 if theme_dict==None:
#                     all_data["theme"]="Unknown"
#                     rootLogger.info("theme {}".format(all_data["theme"]))

                
#                 else:
#                     for i in theme_dict:
#         # if keyword in i push key of i to theme
#                         if keyword in theme_dict[i]:
#                             all_data["theme"]=i
#                             rootLogger.info("theme {}".format(all_data["theme"]))
#                             break
#                         else:
#                             all_data["theme"]="Unknown"
# #if subtheme in theme_dict keys set all_data["theme"]
#else set all_data["theme"] to "Unknown"
                all_data["html"]=news["html"]    
                rootLogger.info("html {}".format(all_data["html"]))                    
                all_data["subtheme"]=keyword
                rootLogger.info("subtheme {}".format(all_data["subtheme"]))
                if isinstance(i["pagemap"],list):
                    if "article:modified_date" in i["pagemap"]["metatags"][0]:
                        all_data["date_published"]=date_time_extract(i["pagemap"]["metatags"][0]["article:modified_date"])
                        rootLogger.info("date_published {}".format(all_data["date_published"]))
                    if 'article:modified_time' in i["pagemap"]["metatags"][0]:
                        rootLogger.info("date_time_extract {}".format(i["pagemap"]["metatags"][0]["article:modified_time"]))
                        all_data["date_published"]=date_time_extract(i["pagemap"]["metatags"][0]['article:modified_time'])
                    elif 'article:published_time' in i["pagemap"]["metatags"][0]:
                        rootLogger.info("date_time_extract {}".format(i["pagemap"]["metatags"][0]["article:published_time"]))
                        all_data["date_published"]=date_time_extract(i["pagemap"]["metatags"][0]['article:published_time'])
                    elif 'article:published_date' in i["pagemap"]["metatags"][0]:
                        rootLogger.info("date_time_extract {}".format(i["pagemap"]["metatags"][0]["article:published_date"]))
                        all_data["date_published"]=date_time_extract(i["pagemap"]["metatags"][0]['article:published_date']) 
                    else:
                        if "ago" not in i["snippet"][:15]:
                            all_data["date_published"]=i["snippet"][:12]
                        
                    #subtract the time in  i["snippet"][:8] to date time now
                        else:
                                if "week" in i["snippet"][:12]:
                                    rootLogger.info("date_time_extract {}".format(i["snippet"][:12]))
                                    all_data["date_published"]=datetime.now()-timedelta(weeks=int(i["snippet"].split(" ")[0]))

                                elif "day" in i["snippet"][:12]:
                                    rootLogger.info("date_time_extract {}".format(i["snippet"][:12]))
                                    all_data["date_published"]=datetime.now()-timedelta(days=int(i["snippet"].split(" ")[0]))
                                elif "hour" in i["snippet"][:12]:
                                    rootLogger.info("date_time_extract {}".format(i["snippet"][:12]))
                                    all_data["date_published"]=datetime.now()-timedelta(hours=int(i["snippet"].split(" ")[0]))
                                elif "minute" in i["snippet"][:12]:
                                    rootLogger.info("date_time_extract {}".format(i["snippet"][:12]))
                                    all_data["date_published"]=datetime.now()-timedelta(minutes=int(i["snippet"].split(" ")[0]))
                                elif "second" in i["snippet"][:12]:
                                    rootLogger.info("date_time_extract {}".format(i["snippet"][:12]))
                                    all_data["date_published"]=datetime.now()-timedelta(seconds=int(i["snippet"].split(" ")[0]))
                                #if all_data["date_published"] is a string convvert it to datetime withdatetime.strptime(all_data["date_published"], "%b %d, %Y")   
                else:
                            if "week" in i["snippet"][:12]:
                                rootLogger.info("date_time_extract {}".format(i["snippet"][:12]))
                                all_data["date_published"]=datetime.now()-timedelta(weeks=int(i["snippet"].split(" ")[0]))

                            elif "day" in i["snippet"][:12]:
                                rootLogger.info("date_time_extract {}".format(i["snippet"][:12]))
                                all_data["date_published"]=datetime.now()-timedelta(days=int(i["snippet"].split(" ")[0]))
                            elif "hour" in i["snippet"][:12]:
                                rootLogger.info("date_time_extract {}".format(i["snippet"][:12]))
                                all_data["date_published"]=datetime.now()-timedelta(hours=int(i["snippet"].split(" ")[0]))
                            elif "minute" in i["snippet"][:12]:
                                rootLogger.info("date_time_extract {}".format(i["snippet"][:12]))
                                all_data["date_published"]=datetime.now()-timedelta(minutes=int(i["snippet"].split(" ")[0]))
                            elif "second" in i["snippet"][:12]:
                                rootLogger.info("date_time_extract {}".format(i["snippet"][:12]))
                                all_data["date_published"]=datetime.now()-timedelta(seconds=int(i["snippet"].split(" ")[0]))
                            #if all_data["date_published"] is a string convvert it to datetime withdatetime.strptime(all_data["date_published"], "%b %d, %Y")   
                            
                
    
                all_data["date_scraped"]=news["date_scraped"]
#if all_data["date_published"] endswith a " "remove it
                             
                if isinstance(all_data["date_published"],str):
                    if all_data["date_published"][-1]==" ":
                        all_data["date_published"]=all_data["date_published"][:-1]  

                    try:
                            all_data["date_published"]=datetime.strptime(all_data["date_published"], "%b %d, %Y")
                    except:
#convert 2022-02-25 10:51:40.834047 to datetime and set equal to all_data["date_published"]                        
                        all_data["date_published"]=datetime.strptime(all_data["date_published"], "%Y-%m-%d %H:%M:%S.%f")        
                try:
                    all_data["language"]=detect(all_data["text"])
                    rootLogger.info("language {}".format(all_data["language"]))
                except:

                    all_data["language"]="Unknown"
                    rootLogger.info("language not detected")  
                cordinates=None    
                try:
                    if all_data["location"]=="story":
                        soup=BeautifulSoup(news["html"], "html.parser")
                        rootLogger.info("soup {}".format(soup))
                        place=soup.findAll("div", {"class":"athr-info"})
                        loc_name=place[0].text.split(" ")[-3][1:]
                        rootLogger.info("loc_name {}".format(loc_name))
                        cordinates=loc.geocode(translator.translate(loc_name, dest='en').text+" "+all_data["state"])
                        all_data["location"]=translator.translate(loc_name, dest='en').text
                        rootLogger.info("location {}".format(all_data["location"]))
                    else:    
                        cordinates=loc.geocode(all_data["location"]+" "+all_data["state"])
                        rootLogger.info("cordinates {}".format(cordinates))

                except:
                    all_data["long"]="Unknown"    
                    all_data["lat"]="Unknown"
                   # cordinates="Unknown"
                if cordinates==None:
                    all_data["long"]="Unknown"    
                    all_data["lat"]="Unknown"
                  #  cordinates="Unknown"    
                if cordinates != "Unknown" :
                    if hasattr(cordinates, 'longitude'):


                        all_data["long"]=cordinates.longitude
                    else:
                        rootLogger.info("longitude not found")
                        all_data["long"]="Unknown"
                    if hasattr(cordinates, 'latitude'):        
                        all_data["lat"]=cordinates.latitude
                    else:
                        rootLogger.info("latitude not found")
                        all_data["lat"]="Unknown"    
                         
                else:
                    all_data["long"]="Unknown"    
                    all_data["lat"]="Unknown"

                all_data["quotes"]=extect_quotes(all_data["text"])
                rootLogger.info("quotes {}".format(all_data["quotes"]))
                # look for images in i["pagemap"]["cse_image"]  retuen the length of the list add to all_data["images_num"] 
                if "cse_image" in i["pagemap"]:
                    rootLogger.info("images_num {}".format(len(i["pagemap"]["cse_image"])))         
                    all_data["images_num"]=len(i["pagemap"]["cse_image"])
                    image_links=[]
                    for j in i["pagemap"]["cse_image"]:
                        
                        image_links.append(j["src"])
                    all_data["image_links"]=image_links
                    #if all_data["images_num"]>0 and all image links dont end with photo.jpg add all_data["imgage_found"]=True else add all_data["image_found"]=False
                    if all_data["images_num"]>0:
                        for j in image_links:
                            if j[-5:]!="photo.jpg":
                                all_data["image_found"]=True
                                break
                            else:
                                all_data["image_found"]=False
                else:
                    all_data["images_num"]=0
                    all_data["image_found"]=False                   
                # remove ,?.! from all_data["text"] and get word count add to all_data["word_count"]
                            
                
                data.append(all_data)
        try:
            if len(search_result['items'])<10:
                break
            else:
                start_index+=10
        
        except:
            break  # if the search result is empty return an empty list      
        
                    
        else:
            data.append({"status":"fail","rsults":search_result["searchInformation"]["totalResults"],"start_index":search_result["queries"]["request"][0]["startIndex"],"search_term":keyword})

    return data


#from a list of dictnaries remove the dictanries that has the fisrt key as "status"
def remove_status(data):
    new_data=[]
    for i in data:
        if "status" not in i and "error" not in i:
            new_data.append(i)
    return new_data

#for a colum in a dataframe replace a string with other string

def replace_string(data,column,old_string,new_string):
    data[column]=data[column].str.replace(old_string,new_string)
    return data
#get location form links in a dataframe by i["link"].split("/")[4].split("-")[0] if Publicaiton is Navbharat Times then get location from i.link.split("/")[5]
def get_location(data):
    if data["publication"]=="Navbharat Times":
        data["location"]=data["link"].split("/")[5]
    else:    
        data["location"]=data["link"].str.split("/")[4].str.split("-")[0]
    #data["location"]=data["location"].str.split("/")[5]
    return data


#if a sql database exitsts then connect to it else create a new database on muSQL server


 

#use sqlalchemy to log into mysql server read confing file using configparser

#create db if not exist
def sql_login(config_file):
    
    config=configparser.ConfigParser()
    config.read(config_file)
    user=config["sql"]["user"]
    password=config["sql"]["password"]
    host=config["sql"]["host"]
    database=config["sql"]["database"]
    engine=create_engine("mysql+pymysql://{}:{}@{}/{}".format(user,password,host,database))

    
    return engine
#create a table in a database using pandas and sqlalchemy
def df_to_sql(data,table_name,engine):
    data.to_sql(table_name,engine,if_exists="append",index=False)   
# in a list of lists append all elememets in the list of list to a new list if "status" and "error" not in the elemet insdie the list of list
# 
def remove_status_from_list(data):
    new_data=[]
    for i in data:
        for j in i:
            if "status" not in j:
                if "error" not in j:
                    new_data.append(j)
               
    return new_data  

def filter_text(df):
    df=df[df["char_count"]>100]
    df=df[~df["link"].str.endswith("news")]
    df=df[~df["link"].str.endswith("news-3")]
    df=df[~df["link"].str.endswith("/")]
    # remove rows where df["publication"]=="The Times of India" and df["char_count"]==582
    df=df[~((df["publication"]=="The Times of India")&(df["char_count"]==582))]
    #if link.split("/")[-2]==articlelist then remove the row
    df=df[~df["link"].str.contains("articlelist")]
    return df
        
#remove rows that end with "news" or "news-3" in a dataframe["text"]
#punctuations = ['nn','n', '।','/', '`', '+', '\', '"', '?', '▁(', '$', '@', '[', '_', "'", '!', ',', ':', '^', '|', ']', '=', '%', '&', '.', ')', '(', '#', '*', '', ';', '-', '}','|','"'] write a 
#function that removes punctuations from a string
def remove_punctuations(text):
    punctuations = ['nn','n', '।','/', '`', '+', '\'', '"', '?', '▁(', '$', '@', '[', '_', "'", '!', ',', ':', '^', '|', ']', '=', '%', '&', '.', ')', '(', '#', '*', '', ';', '-', '}','|','"']
    for i in punctuations:
        text=text.replace(i,"")
    return text
#remove joining words form the list stopwords_hi = ['तुम','मेरी','मुझे','क्योंकि','हम','प्रति','अबकी','आगे','माननीय','शहर','बताएं','कौनसी','क्लिक','किसकी','बड़े','मैं','and','रही','आज','लें','आपके','मिलकर','सब','मेरे','जी','श्री','वैसा','आपका','अंदर', 'अत', 'अपना', 'अपनी', 'अपने', 'अभी', 'आदि', 'आप', 'इत्यादि', 'इन', 'इनका', 'इन्हीं', 'इन्हें', 'इन्हों', 'इस', 'इसका', 'इसकी', 'इसके', 'इसमें', 'इसी', 'इसे', 'उन', 'उनका', 'उनकी', 'उनके', 'उनको', 'उन्हीं', 'उन्हें', 'उन्हों', 'उस', 'उसके', 'उसी', 'उसे', 'एक', 'एवं', 'एस', 'ऐसे', 'और', 'कई', 'कर','करता', 'करते', 'करना', 'करने', 'करें', 'कहते', 'कहा', 'का', 'काफ़ी', 'कि', 'कितना', 'किन्हें', 'किन्हों', 'किया', 'किर', 'किस', 'किसी', 'किसे', 'की', 'कुछ', 'कुल', 'के', 'को', 'कोई', 'कौन', 'कौनसा', 'गया', 'घर', 'जब', 'जहाँ', 'जा', 'जितना', 'जिन', 'जिन्हें', 'जिन्हों', 'जिस', 'जिसे', 'जीधर', 'जैसा', 'जैसे', 'जो', 'तक', 'तब', 'तरह', 'तिन', 'तिन्हें', 'तिन्हों', 'तिस', 'तिसे', 'तो', 'था', 'थी', 'थे', 'दबारा', 'दिया', 'दुसरा', 'दूसरे', 'दो', 'द्वारा', 'न', 'नहीं', 'ना', 'निहायत', 'नीचे', 'ने', 'पर', 'पर', 'पहले', 'पूरा', 'पे', 'फिर', 'बनी', 'बही', 'बहुत', 'बाद', 'बाला', 'बिलकुल', 'भी', 'भीतर', 'मगर', 'मानो', 'मे', 'में', 'यदि', 'यह', 'यहाँ', 'यही', 'या', 'यिह', 'ये', 'रखें', 'रहा', 'रहे', 'ऱ्वासा', 'लिए', 'लिये', 'लेकिन', 'व', 'वर्ग', 'वह', 'वह', 'वहाँ', 'वहीं', 'वाले', 'वुह', 'वे', 'वग़ैरह', 'संग', 'सकता', 'सकते', 'सबसे', 'सभी', 'साथ', 'साबुत', 'साभ', 'सारा', 'से', 'सो', 'ही', 'हुआ', 'हुई', 'हुए', 'है', 'हैं', 'हो', 'होता', 'होती', 'होते', 'होना', 'होने', 'अपनि', 'जेसे', 'होति', 'सभि', 'तिंहों', 'इंहों', 'दवारा', 'इसि', 'किंहें', 'थि', 'उंहों', 'ओर', 'जिंहें', 'वहिं', 'अभि', 'बनि', 'हि', 'उंहिं', 'उंहें', 'हें', 'वगेरह', 'एसे', 'रवासा', 'कोन', 'निचे', 'काफि', 'उसि', 'पुरा', 'भितर', 'हे', 'बहि', 'वहां', 'कोइ', 'यहां', 'जिंहों', 'तिंहें', 'किसि', 'कइ', 'यहि', 'इंहिं', 'जिधर', 'इंहें', 'अदि', 'इतयादि', 'हुइ', 'कोनसा', 'इसकि', 'दुसरे', 'जहां', 'अप', 'किंहों', 'उनकि', 'भि', 'वरग', 'हुअ', 'जेसा', 'नहिं']#remove punctuations from a list of strings
def remove_join_words_hi(text):
    stopwords_hi = ['तुम','मेरी','मुझे','क्योंकि','हम','प्रति','अबकी','आगे','माननीय','शहर','बताएं','कौनसी','क्लिक','किसकी','बड़े','मैं','and','रही','आज','लें','आपके','मिलकर','सब','मेरे','जी','श्री','वैसा','आपका','अंदर', 'अत', 'अपना', 'अपनी', 'अपने', 'अभी', 'आदि', 'आप', 'इत्यादि', 'इन', 'इनका', 'इन्हीं', 'इन्हें', 'इन्हों', 'इस', 'इसका', 'इसकी', 'इसके', 'इसमें', 'इसी', 'इसे', 'उन', 'उनका', 'उनकी', 'उनके', 'उनको', 'उन्हीं', 'उन्हें', 'उन्हों', 'उस', 'उसके', 'उसी', 'उसे', 'एक', 'एवं', 'एस', 'ऐसे', 'और', 'कई', 'कर','करता', 'करते', 'करना', 'करने', 'करें', 'कहते', 'कहा', 'का', 'काफ़ी', 'कि', 'कितना', 'किन्हें', 'किन्हों', 'किया', 'किर', 'किस', 'किसी', 'किसे', 'की', 'कुछ', 'कुल', 'के', 'को', 'कोई', 'कौन', 'कौनसा', 'गया', 'घर', 'जब', 'जहाँ', 'जा', 'जितना', 'जिन', 'जिन्हें', 'जिन्हों', 'जिस', 'जिसे', 'जीधर', 'जैसा', 'जैसे', 'जो', 'तक', 'तब', 'तरह', 'तिन', 'तिन्हें', 'तिन्हों', 'तिस', 'तिसे', 'तो', 'था', 'थी', 'थे', 'दबारा', 'दिया', 'दुसरा', 'दूसरे', 'दो', 'द्वारा', 'न', 'नहीं', 'ना', 'निहायत', 'नीचे', 'ने', 'पर', 'पर', 'पहले', 'पूरा', 'पे', 'फिर', 'बनी', 'बही', 'बहुत', 'बाद', 'बाला', 'बिलकुल', 'भी', 'भीतर', 'मगर', 'मानो', 'मे', 'में', 'यदि', 'यह', 'यहाँ', 'यही', 'या', 'यिह', 'ये', 'रखें', 'रहा', 'रहे', 'ऱ्वासा', 'लिए', 'लिये', 'लेकिन', 'व', 'वर्ग', 'वह', 'वह', 'वहाँ', 'वहीं', 'वाले', 'वुह', 'वे', 'वग़ैरह', 'संग', 'सकता', 'सकते', 'सबसे', 'सभी', 'साथ', 'साबुत', 'साभ', 'सारा', 'से', 'सो', 'ही', 'हुआ', 'हुई', 'हुए', 'है', 'हैं', 'हो', 'होता', 'होती', 'होते', 'होना', 'होने', 'अपनि', 'जेसे', 'होति', 'सभि', 'तिंहों', 'इंहों', 'दवारा', 'इसि', 'किंहें', 'थि', 'उंहों', 'ओर', 'जिंहें', 'वहिं', 'अभि', 'बनि', 'हि', 'उंहिं', 'उंहें', 'हें', 'वगेरह', 'एसे', 'रवासा', 'कोन', 'निचे', 'काफि', 'उसि', 'पुरा', 'भितर', 'हे', 'बहि', 'वहां', 'कोइ', 'यहां', 'जिंहों', 'तिंहें', 'किसि', 'कइ', 'यहि', 'इंहिं', 'जिधर', 'इंहें', 'अदि', 'इतयादि', 'हुइ', 'कोनसा', 'इसकि', 'दुसरे', 'जहां', 'अप', 'किंहों', 'उनकि', 'भि', 'वरग', 'हुअ', 'जेसा', 'नहिं']
    for i in stopwords_hi:
        text=text.replace(i,"")
    return text


 #count the number of words seprated by space in a string
def count_words(text):
    text=remove_punctuations(text)
    text=text.split()
    return len(text)
#count unique words in a string
def count_unique_words(text):
    text=remove_punctuations(text)
    text=text.split()
    return len(set(text))
   
#take a dataframe read df["text"] and count the number of words in each row and add it to df["word_count"]

def add_word_count(df):
    df["word_count"]=df["text"].apply(count_words)
    return df
#write a fuction that returns a dictionary of unique words and their count in a string

#for i in df["text"]:      #for each row in df (i.e. each text) use the function count_unique_words_in_text to get a dictionary of unique words and their count and pass it to a new calumn in df called "word_count"




    
        
def get_pos_from_text_hi(text,lang):
    text=remove_punctuations(text)
    nlp = stanza.Pipeline(lang=lang, processors='tokenize,pos')
    doc = nlp(text)
    text_lis=[]
    pos=[]
    for sent in doc.sentences:
        for word in sent.words:
            text_lis.append(word.text)
            pos.append(word.upos)
    #count unique words in text test_lis 
    count=Counter(text.split())
    final_dict={}

    for i,j in count.items():
        if i in text_lis:
            final_dict[i]=[j,pos[text_lis.index(i)]]
    #sort dict in decending order usign count
    final_dict=sorted(final_dict.items(), key=lambda kv: kv[1][0], reverse=True)  
    #convert final_dict to a dictionary
    #       
    return dict(final_dict)


# after geting pos form text check for nouns and verbs
def get_top_words_hi_nouns(text,df=None):
    if df:
        nouns_and_count={}
        for i in df["pos"]:
            if i[1]=="NOUN":
                nouns_and_count[i[0]]=i[2]
        return nouns_and_count
    else:    
                

        words=get_pos_from_text_hi(text,f"hi")
        nouns_and_count={}
        for i in words:
            if words[i][1]=="NOUN":
                nouns_and_count[i]=words[i][0]
        return nouns_and_count


def get_top_words_hi_verbs(text=None,df=None):
    if df is not None:
        verbs_and_count={}
        for i in df["pos"]:
            if i[1]=="VERB":
                verbs_and_count[i[0]]=i[2]
                return verbs_and_count
    else:
        words=get_pos_from_text_hi(text,"hi")
        verbs_and_count={}
        for i in words:
            if words[i][1]=="VERB":
                verbs_and_count[i]=words[i][0]
        return verbs_and_count

def get_top_words_en_noun(text,df=None):
    if df:
        file_id=df["file_id"][0]
        request = drive_service.files().update(fileId=file_id, body=file_metadata, media_body=media)
    else:
        request = drive_service.files().create(body=file_metadata, media_body=media)
    response = request.execute()
    return response

    
        
    #split a dataseries and get the last element
    df.str.split(' ').str.get(-1)
    #set the dictonary in decendign order sorting the values
    my_dict=dict(sorted(my_dict.items(), key=lambda kv: kv[1], reverse=True))
    
        

        

#take a dataframe read df["text"] and depending on df[language] if hi use hi if en use en
#  get top 5 adjectives nouns and verbs and add it to df["top_adjectives"],df["top_nouns"],df["top_verbs"]


def add_top_words(df):
    if df["language"]=="hi":
        df["top_adjectives"]=df["text"].apply(get_top_words_hi_adjectives)
        df["top_nouns"]=df["text"].apply(get_top_words_hi_nouns)
        df["top_verbs"]=df["text"].apply(get_top_words_hi_verbs)
    else:
        df["top_adjectives"]=df["text"].apply(get_top_words_en_adjectives)
        df["top_nouns"]=df["text"].apply(get_top_words_en_nouns)
        df["top_verbs"]=df["text"].apply(get_top_words_en_verbs)
    return df
#using stanza libiary and count_unique_words function to get the top 5 adjectives nouns and verbs with there number of occurences
#for hi
# and en

def get_top_words_hi_adjectives(text):
    text=remove_punctuations(text)
    #text=text.split()
    nlp=stanza.Pipeline(lang="hi")
    doc=nlp(text)
    word_dict=count_unique_words_in_text(text)
    top_words=[]
    for i in doc.sentences[0].to_dict():
        if i["upos"]=="ADJ":
            top_words.append(i["lemma"])
    for i in top_words:
        if i in word_dict:
            word_dict[i]=word_dict[i]-1
    return word_dict
#check for dublicate links in df["link"]
#if there is a duplicate merge the columms df["subthemes"] with a coma seprating the values
#for every oher column in df keep the first value
#return the df
def check_duplicate_links(df):
    df=df.groupby("link").agg({'state':"first", 'publication':"first", 'link':"first", 'location':"first", 'title':"first", 'text':"first",
       'char_count':"first", 'date_published':"first", 'date_scraped':"first", 'language':"first",
       'long':"first", 'lat':"first", 'quotes':"first", 'images_num':"first", 'image_links':"first", 'image_found':"first","subtheme":lambda x:','.join(x.values)})
    #add other cloums to df with the first value
    return df
    

def check_duplicate_text(df):
    df=df.groupby("text").agg({'state':"first", 'publication':"first", 'link':"first", 'location':"first", 'title':"first", 'text':"first",
         'char_count':"first", 'date_published':"first", 'date_scraped':"first", 'language':"first",  
            'long':"first", 'lat':"first", 'quotes':"first", 'images_num':"first", 'image_links':"first", 'image_found':"first","subtheme":lambda x:','.join(x.values)})


    return df


    #use listdir to get all the files form a directory 
    #then check weather the file is a csv file or not
    #if csv read the file with pandas.read_csv
    #if not skip it
    #concatnate all the files read to a single dataframe
def read_files(path):
    files=os.listdir(path)
    df=pandas.DataFrame()
    for i in files:
        if i.endswith(".csv"):
            df=pandas.concat([df,pandas.read_csv(path+i)])
    return df

 #write a fuction df check
 # wehere given a dictionary of lists
 # check check weter all the strings found in the list are in df["text"]
 #if there is a space between the string and the text
 #split and search each part saperatly
 #set both the values to lowercase before checking
 #if none of the strings are found remove the row from df
 #return df
def df_check(df,theme_dict):
    all_themes=[]
    lang_dict=dict(zip(df.text,df.language))
    
    for t in df["text"] :

        for i in theme_dict:
            for j in theme_dict[i]:
                themes=[]
            
                if lang_dict[t]=="en":
                    
                    if " " in j:
                        x=j.split(" ")
                        for k in x:
                            if k.lower() in t.lower():
                                themes.append(j)
                    else:
                        if j.lower() in t.lower():
                            themes.append(j)
                else:
                    if " " in j:
                        x=j.split(" ")
                        for k in x:
                            
                            translated=transliterate(k, sanscript.ITRANS, sanscript.DEVANAGARI)
                            if translated.lower() in t.lower():
                                themes.append(j)
                    else:
                        translated=transliterate(j, sanscript.ITRANS, sanscript.DEVANAGARI)
                        if translated.lower() in t.lower():
                            themes.append(j)            
        all_themes.append(themes)   
        
    df["final_theme"]=all_themes
    return df                        


                
                
            
                            

                    
    #if final_themes is empty remove the row
#    df=df[df["final_themes"].notnull()]
    #append all_themes to the row
    df["final_themes"]=df["final_themes"].apply(lambda x:','.join(x))
    return df            


#the df if df["publication"]=="Amar Ujala"
#split the text by "}" and set last elemet of the list to df["text"]
#return df
def remove_brackets(df):
    dfx=df[df["publication"]=="Amar Ujala"]
    dfx["text"]=dfx["text"].str.split("}").str.get(-1)
    dfy=df[df["publication"]!="Amar Ujala"]
    df=pandas.concat([dfx,dfy])
    return df
#write a regular expression to remove the text between the brackets
#return df
def remove_brackets_regex(df):
    df["text"]=df["text"].str.replace(r"\{(.*?)\}\}", "")
    return df