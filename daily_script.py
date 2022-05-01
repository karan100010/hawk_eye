import pandas
from base import *
from themes import theme_dict
from datetime import datetime

def get_data():
    all_data=[]
    for i in theme_dict.keys():
        for j in theme_dict[i]:
            all_data.append(get_full_data(j,"hawk_eye/scraper.conf",theme_dict=theme_dict,days=1))
    return all_data
all_data=get_data()
all_data_clean=remove_status(all_data)
df=pandas.DataFrame(all_data_clean)
#get dataframe to csv with the time stamp of the day
df.to_csv("C:/Users/karan/daily_data.csv",index=False)
