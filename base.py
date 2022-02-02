#write a fuction that takes google sheets as input and returns a json object
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from newspaper import Article
from datetime import datetime   
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




    
    