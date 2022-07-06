import pandas
from base import *
from themes import theme_dict
from datetime import datetime
import stanza
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
df=check_duplicate_text(df)
df=check_duplicate_links(df)
df=remove_brackets_regex(df)
name="daily_data"+datetime.now().strftime("%Y-%m-%d")+".csv"
df=df[~df["text"].str.lower().str.contains("gyanvapi")]


#get dataframe to csv with the time stamp of the day
df.to_csv(name,index=False)

nlp=stanza.Pipeline(lang="en",processors='tokenize,pos')

df_hi=df[df["language"]=="hi"]
df_en=df[df["language"]=="en"]
df_en["pos"]=df_en.text.apply(get_pos_from_text_hi,nlp=nlp)
nlp=stanza.Pipeline(lang="en",processors='tokenize,pos')
df_hi["pos"]=df_hi.text.apply(get_pos_from_text_hi,nlp=nlp)

df=pandas.concat([df_hi,df_en])

df["noun"]=df.pos.apply(get_nouns)
df["propnouns"]=df.pos.apply(get_propernouns)
df["word_count_nouns"]=df.noun.apply(get_wordcloud_string)
df["word_count_propnouns"]=df.propnouns.apply(get_wordcloud_string)
df["word_count_nouns"]=df.word_count_nouns.str.replace("ad","")
df["dates"]=df.date_published.apply(lambda x: x.split()[0])
dff=pandas.read_csv("final_may.csv")
dfx=pandas.concat(df,dff)
dfx.to_csv("final_may.csv",index=False)