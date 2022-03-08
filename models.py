from datetime import date
from unicodedata import category
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,DateTime
from sqlalchemy.orm import relationship

from .database import Base


class NewsItems(Base):
    __tablename__ = "news_items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    link= Column(String)
    text= Column(String)
    state= Column(String)
    category= Column(String)
    subtheme= Column(String)
    data_scraped= Column(DateTime)
    data_published= Column(DateTime)
    language= Column(String)
    location= Column(String)
    long= Column(String)
    lat= Column(String)
    quotes= Column(String)
    image_num= Column(Integer)
    image_url= Column(String)
    image_found= Column(Boolean)
    publication= Column(String)





  

    news_items = relationship("newsdata")




