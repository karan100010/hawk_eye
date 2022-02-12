#write a fuction that takes google sheets as input and returns a json object
import googletrans
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from newspaper import Article
import requests
from datetime import datetime, timedelta
import pandas 
from googletrans import Translator
import re
from text_based_func import *

def read_google_sheet_to_json(sheet):
   
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name( secret_key,scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet).sheet1
    data = sheet.get_all_records()
    return data


 # given a link scrape the news,title,date_published artical using the newspaper3k library and return a json object

def news_scraper(link):
    article = Article(link)
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
    
    

 #create a postgresql table 


#create a fuction that takes a list of json objects ,name of the table and user and inserts them into a postgresql table three parameters link,title,text


#search a term with google search api in python
#restrict the serch to only the past week
def search(term,cx,days=7,start_index=0):        
    search_url = "https://www.googleapis.com/customsearch/v1?key=AIzaSyAT6MMtfiG24pdVoF8Fh3pYLgkZr7Zm39c&cx={}&q={}&start={}&dateRestrict=d{}".format(cx,term,start_index,days)
    response = requests.get(search_url)
    return response.json()

def get_links(term,cx):
    page_index=0
    all_links=[]
    while True:
        search_url = "https://www.googleapis.com/customsearch/v1?key=AIzaSyAT6MMtfiG24pdVoF8Fh3pYLgkZr7Zm39c&cx={}&q={}&start={}".format(cx,term,page_index)
        response = requests.get(search_url)
        json_response = response.json()
        try:
            links=[i['link'] for i in json_response['items']]
        except:
            logger.info("Error in getting links")
            return all_links    
        all_links=all_links+links
        logger.info(len(all_links))
        if len(links)<10:
            logger.info("done")
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

def get_full_data(cx,keyword,days=30,start_index=0,theme_dict=None):
    data=[]
    
    search_result=search(keyword,cx=cx,days=days,start_index=start_index)
    if search_result["queries"]["request"][0]["totalResults"]>0:
        data.append({"status":"success","rsults":search_result["queries"]["request"][0]["totalResults"],"start_index":search_result["queries"]["request"][0]["startIndex"],"search_term":keyword})
        for i in search_result['items']:
            
            all_data={}
            all_data["State"]="Uttar Pradesh"
            try:
                all_data["Publication"]=i["pagemap"]["metatags"][0]["og:site_name"]
            except:
                all_data["Publication"]="Unknown"
            try:
                all_data["language"]=i["pagemap"]["metatags"][0]["og:locale"].split("_")[0]
            except:
                all_data["language"]="Unknown"

            try:
                all_data["link"]=i["link"]
            except:
                all_data["link"]="Unknown"
            if all_data["link"]!="Unknown":
                news_scraper=news_scraper(all_data["link"])
                all_data["title"]=news_scraper["title"]
                all_data["text"]=news_scraper["text"]
                all_data["date_scraped"]=news_scraper["date_scraped"]
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
                if i["pagemap"]["metatags"][0]['article:modified_time']:
                    all_data["date_published"]=date_time_extract(i["pagemap"]["metatags"][0]['article:modified_time'])
                elif i["pagemap"]["metatags"][0]['article:published_time']:
                    all_data["date_published"]=date_time_extract(i["pagemap"]["metatags"][0]['article:published_time'])
                elif i["pagemap"]["metatags"][0]['article:published_date']:
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

            data.append(all_data)
              
    else:
        data.append({"status":"fail","rsults":search_result["queries"]["request"][0]["totalResults"],"start_index":search_result["queries"]["request"][0]["startIndex"],"search_term":keyword})

    return all_data







    
