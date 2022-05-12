import pandas
from base import *
from themes import theme_dict
from datetime import datetime

def get_data():
    all_data=[]
    for i in theme_dict:
    
        for j in theme_dict[i]:
            all_data.append(get_full_data(j,"hawk_eye/scraper.conf",theme_dict=theme_dict,days=1))
    return all_data
    
all_data=get_data()
data=[]
for i in all_data:
    for j in i:
        data.append(j)
all_data_clean=remove_status(data)  

df=pandas.DataFrame(all_data_clean)
df=filter_text(df)
df=check_duplicate_links(df)
name="daily_data"+datetime.now().strftime("%Y-%m-%d")+".csv"

#get dataframe to csv with the time stamp of the day
df.to_csv(name,index=False)
