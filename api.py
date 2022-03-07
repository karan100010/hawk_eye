from fastapi import FastAPI
from base import *
import configparser
import logging
from sqlalchemy import create_engine


app= FastAPI()
# read config file
# 
config = configparser.ConfigParser()

