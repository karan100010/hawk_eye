from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#join the directory one level up
import os,sys
sys.path.append("..")

from base import sql_login
sys.path.append("api")


engine = sql_login("../scraper.conf")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
