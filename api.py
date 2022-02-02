from fastapi import FastAPI
from base import *

app= FastAPI()
# return the table named news as a json object
@app.get("/")
def index():
    
    


@app.post("/")

def post(data,table_name):
    conn = psycopg2.connect(dbname="newsdb", user="postgres", password="postgres", host="localhost", port="5432")
    cur = conn.cursor()
    
   
    cur.execute("CREATE TABLE "+table_name+" (id serial PRIMARY KEY, title varchar, link varchar, date varchar, text varchar)")
    for i in range(len(data)):
        cur.execute("INSERT INTO "+table_name+" (title, link, date, text) VALUES (%s, %s, %s, %s)", (data[i]['title'], data[i]['link'], data[i]['date'], data[i]['text']))
    conn.commit()
    cur.close()
    conn.close() 


@app.delete("/")

def delete_table(table_name):
    conn = psycopg2.connect(dbname="newsdb", user="postgres", password="postgres", host="localhost", port="5432")
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS "+table_name)
    conn.commit()
    cur.close()
    conn.close()







    