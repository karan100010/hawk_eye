from sqlalchemy.orm import Session

from . import models


def get_data(db: Session, NewsItems_id: int):
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
