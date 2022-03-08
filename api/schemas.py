from typing import List, Optional

from pydantic import BaseModel

#write schemas for NewsItems
class NewsItems(BaseModel):
    id: int
    title: str
    link: str
    text: str
    state: str
    category: str
    subtheme: str
    data_scraped: str
    data_published: str
    language: str
    location: str
    long: str
    lat: str
    quotes: str
    image_num: int
    image_url: str
    image_found: bool
    publication: str
    theme: str

 # write schemas for NewsItemsUpdate
class NewsItemsUpdate(BaseModel):
    title: Optional[str] = None
    link: Optional[str] = None
    text: Optional[str] = None
    state: Optional[str] = None
    category: Optional[str] = None
    subtheme: Optional[str] = None
    data_scraped: Optional[str] = None
    data_published: Optional[str] = None
    language: Optional[str] = None
    location: Optional[str] = None
    long: Optional[str] = None
    lat: Optional[str] = None
    quotes: Optional[str] = None
    image_num: Optional[int] = None
    image_url: Optional[str] = None
    image_found: Optional[bool] = None
    publication: Optional[str] = None   
    theme: Optional[str] = None

#write schemas for NewsItemsCreate
class NewsItemsCreate(BaseModel):
    title: str
    link: str
    text: str
    state: str
    category: str
    subtheme: str
    data_scraped: str
    data_published: str
    language: str
    location: str
    long: str
    lat: str
    quotes: str
    image_num: int
    image_url: str
    image_found: bool
    publication: str
    theme: str

 # write schemas for NewsItemsInDB
