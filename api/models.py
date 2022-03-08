from datetime import date
from unicodedata import category
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,DateTime
from sqlalchemy.orm import relationship

from database import Base


class NewsItems(Base):
    __tablename__ = "news_items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(32))
    link= Column(String(32))
    text= Column(String(32))
    state= Column(String(32))
    category= Column(String(32))
    subtheme= Column(String(32))
    data_scraped= Column(DateTime)
    data_published= Column(DateTime)
    language= Column(String(32))
    location= Column(String(32))
    long= Column(String(32))
    lat= Column(String(32))
    quotes= Column(String(32))
    image_num= Column(Integer)
    image_url= Column(String(32))
    image_found= Column(Boolean)
    publication= Column(String(32))
  

    news_items = relationship("newsdata")




