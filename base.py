#write a fuction that takes google sheets as input and returns a json object
from asyncio.log import logger
from msilib import add_data
import googletrans
import gspread
from matplotlib import image
from oauth2client.service_account import ServiceAccountCredentials
from newspaper import Article
import requests
from datetime import datetime, timedelta
import pandas 
from googletrans import Translator
import re
from text_based_func import *
import logging
from time import sleep
import configparser
#configure logger to print to file and console

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()

fileHandler = logging.FileHandler("{0}/{1}.log".format(".", "log"))
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)
rootLogger.info("Started")
# baselogger = logging.getLogger('base')
translater=Translator()

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
        article.download()
    
        article.parse()
        article.nlp()
        data = {
            'title': article.title,
            'link': link,
            'date': article.publish_date,
            'text': article.text,
            "summary": article.summary,
        "date_scraped": datetime.now()  }
        return data
    else:
        return {}       
    

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


#converting a dataframe with columns links, discription ,text ,title to a dataframe with columns links, discription ,text ,title, category
# into a rss stream
def to_rss(df):
    rss_stream=[]
    for i in df.index:
        rss_stream.append({"link":df.loc[i,"link"],"description":df.loc[i,"description"],"text":df.loc[i,"text"],"title":df.loc[i,"title"],"category":df.loc[i,"category"]})
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

# read cx,keyword,days=30,start_index,theme_dict form a config file using config parser
def get_full_data(keyword,conf_file,theme_dict,start_index=0,days=30):

    config = configparser.ConfigParser()
    config.read(conf_file)
    cx=config['Arguments']['cx']
   
    api_key=config['Arguments']['api_key']
    #theme_dict=config['Arguments']['theme_dict']

    data=[]
    logging.info("getting links")

    while True: 
        search_result=search(keyword,cx=cx,days=days,start_index=start_index,api_key=api_key)
        logging.info("got links")
        
  #incriment the start index by 10 each time till you get less than 10 links
        try:
            if len(search_result['items'])<10:
                break
            else:
                start_index+=10
        
        except:
            break  # if the search result is empty return an empty list      

        if int(search_result["searchInformation"]["totalResults"])>0:
            data.append({"status":"success","rsults":search_result["searchInformation"]["totalResults"],"start_index":search_result["queries"]["request"][0]["startIndex"],"search_term":keyword})
            for i in search_result['items']:
                
                all_data={}
                all_data["State"]="Uttar Pradesh"
                try:
                    if "og:site_name" in i["pagemap"]["metatags"][0]:
                        all_data["Publication"]=i["pagemap"]["metatags"][0]["og:site_name"]
                    else:
                        all_data["Publication"]=i['displayLink'].split(".")[1]     
                except:
                    all_data["Publication"]="Unknown"
               

                try:
                    all_data["link"]=i["link"]
                except:
                    all_data["link"]="Unknown"
                if all_data["Publication"]=="Navbharat Times":
                    all_data["location"]=all_data["link"].split("/")[5]
                else:
                    all_data["location"]=all_data["link"].split("/")[4].split("-")[0]

                if all_data["link"]!="Unknown":
                    news=news_scraper(all_data["link"])
                    if news:
                        all_data["title"]=news["title"]
                        all_data["text"]=news["text"]
                        all_data["date_scraped"]=news["date_scraped"]
                    else:
                        all_data["title"]="Unknown"
                        all_data["text"]="Unknown"
                        all_data["date_scraped"]="Unknown"    
                else:
                    all_data["title"]="Unknown"
                    all_data["text"]="Unknown"
                    all_data["date_scraped"]="Unknown" 
                    if theme_dict==None:
                        all_data["category"]="Unknown"
                        
                    else:
                        for i in theme_dict:
            # if keyword in i push key of i to category
                            if keyword in theme_dict[i]:
                                all_data["category"]=i
                                break
                            else:
                                all_data["category"]="Unknown"
                all_data["subtheme"]=keyword
                if 'article:modified_time' in i["pagemap"]["metatags"][0]:
                    all_data["date_published"]=date_time_extract(i["pagemap"]["metatags"][0]['article:modified_time'])
                elif 'article:published_time' in i["pagemap"]["metatags"][0]:
                    all_data["date_published"]=date_time_extract(i["pagemap"]["metatags"][0]['article:published_time'])
                elif 'article:published_date' in i["pagemap"]["metatags"][0]:
                    all_data["date_published"]=date_time_extract(i["pagemap"]["metatags"][0]['article:published_date']) 
                else:
                    if "ago" not in i["snippet"][:12]:
                        all_data["date_published"]=i["snippet"][:12]
                #subtract the time in  i["snippet"][:8] to date time now
                    else:
                        if "week" in i["snippet"][:12]:
                            all_data["date_published"]=datetime.now()-timedelta(weeks=int(i["snippet"].split(" ")[0]))

                        elif "day" in i["snippet"][:12]:
                            all_data["date_published"]=datetime.now()-timedelta(days=int(i["snippet"].split(" ")[0]))
                        elif "hour" in i["snippet"][:12]:
                            all_data["date_published"]=datetime.now()-timedelta(hours=int(i["snippet"].split(" ")[0]))
                        elif "minute" in i["snippet"][:12]:
                            all_data["date_published"]=datetime.now()-timedelta(minutes=int(i["snippet"].split(" ")[0]))
                        elif "second" in i["snippet"][:12]:
                            all_data["date_published"]=datetime.now()-timedelta(seconds=int(i["snippet"].split(" ")[0]))
                all_data["date_scraped"]=news["date_scraped"]
                try:
                    all_data["language"]=translater.detect(all_data["text"]).lang
                except:
                    all_data["language"]="Unknown"
                    logger.info("language not detected")    

                all_data["quotes"]=extect_quotes(all_data["text"])
                # look for images in i["pagemap"]["cse_image"]  retuen the length of the list add to all_data["images_num"]          
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
                # remove ,?.! from all_data["text"] and get word count add to all_data["word_count"]
                            
                
                data.append(all_data)
                    
        else:
            data.append({"status":"fail","rsults":search_result["searchInformation"]["totalResults"],"start_index":search_result["queries"]["request"][0]["startIndex"],"search_term":keyword})

    return data

#from a list of dictnaries remove the dictanries that has the fisrt key as "status"
def remove_status(data):
    new_data=[]
    for i in data:
        if "status" not in i:
            new_data.append(i)
    return new_data

#for a colum in a dataframe replace a string with other string

def replace_string(data,column,old_string,new_string):
    data[column]=data[column].str.replace(old_string,new_string)
    return data
#get location form links in a dataframe by i["link"].split("/")[4].split("-")[0] if Publicaiton is Navbharat Times then get location from i.link.split("/")[5]
def get_location(data):
    if data["Publication"]=="Navbharat Times":
        data["Location"]=data["link"].split("/")[5]
    else:    
        data["location"]=data["link"].str.split("/")[4].str.split("-")[0]
    #data["location"]=data["location"].str.split("/")[5]
    return data
   