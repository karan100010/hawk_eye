from sqlalchemy.orm import Session
from fastapi import HTTPException

import models

# add get_all_NewsItems with skip and limit
def get_all_NewsItems(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.NewsItems).offset(skip).limit(limit).all()

def get_data(db: Session, NewsItems_id: int,skip: int = 0):
    return db.query(models.NewsItems).filter(models.NewsItems.id == NewsItems_id).first()


def get_NewsItems_by_link(db: Session, link: str):
    return db.query(models.NewsItems).filter(models.NewsItems.link == link).first()


# insert a list of objects into the database
def create_NewsItems_list(db: Session, NewsItems_list: list):
    db.add_all(NewsItems_list)
    db.commit()
    db.refresh(NewsItems_list)
    return NewsItems_list
    
def create_NewsItems(db: Session, NewsItems: models.NewsItems):
    db.add(NewsItems)
    db.commit()
    db.refresh(NewsItems)
    return NewsItems
#get news items by id
def get_NewsItems(db: Session, NewsItems_id: int):
    return db.query(models.NewsItems).filter(models.NewsItems.id == NewsItems_id).first()

#put news items by link
def update_NewsItems_by_link(db: Session, link: str, NewsItems: models.NewsItems):
    NewsItems_link = get_NewsItems_by_link(db=db, link=link)
    if NewsItems_link is None:
        raise HTTPException(status_code=404, detail="NewsItems not found")
    NewsItems.id = NewsItems_link.id
    db.add(NewsItems)
    db.commit()
    db.refresh(NewsItems)
    return NewsItems

 #get data by subtheme
def get_NewsItems_by_subtheme(db: Session, subtheme: str):
    return db.query(models.NewsItems).filter(models.NewsItems.subtheme == subtheme).all()   

#get data by theme
def get_NewsItems_by_theme(db: Session, theme: str):
    return db.query(models.NewsItems).filter(models.NewsItems.theme == theme).all()    

# add get_all_NewsItems_by_theme
def get_all_NewsItems_by_theme(db: Session, theme: str):
    return db.query(models.NewsItems).filter(models.NewsItems.theme == theme).all()
# add get_all_NewsItems with skip and limit
def get_all_NewsItems(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.NewsItems).offset(skip).limit(limit).all()
