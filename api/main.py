from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session


import crud, models,schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# add a new NewsItems in "/NewsItems"
@app.post("/NewsItems", response_model=schemas.NewsItems, status_code=201)
def create_NewsItems(NewsItems: schemas.NewsItemsCreate, db: Session = Depends(get_db)):
    return crud.create_NewsItems(db=db, NewsItems=NewsItems)

#add multiple new NewsItems in "/NewsItems"
@app.post("/NewsItems/list", response_model=List[schemas.NewsItems], status_code=201)
def create_NewsItems_list(NewsItems_list: List[schemas.NewsItemsCreate], db: Session = Depends(get_db)):
    return crud.create_NewsItems_list(db=db, NewsItems_list=NewsItems_list)

# get a NewsItems by id in "/NewsItems/{id}"
@app.get("/NewsItems/{id}", response_model=schemas.NewsItems)
def read_NewsItems(id: int, db: Session = Depends(get_db)):
    NewsItems = crud.get_NewsItems(db=db, id=id)
    if NewsItems is None:
        raise HTTPException(status_code=404, detail="NewsItems not found")
    return NewsItems

#put a NewsItems by id in "/NewsItems/{id}"
@app.put("/NewsItems/{id}", response_model=schemas.NewsItems)
def update_NewsItems(id: int, NewsItems: schemas.NewsItemsUpdate, db: Session = Depends(get_db)):
    NewsItems_id = crud.get_NewsItems(db=db, id=id)
    if NewsItems_id is None:
        raise HTTPException(status_code=404, detail="NewsItems not found")
    return crud.update_NewsItems(db=db, id=id, NewsItems=NewsItems)
#get all news items


@app.get("/NewsItems", response_model=List[schemas.NewsItems])
def read_all_NewsItems(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    NewsItems = crud.get_all_NewsItems(db=db, skip=skip, limit=limit)
    return NewsItems


#delete a NewsItems by id in "/NewsItems/{id}"
@app.delete("/NewsItems/{id}", status_code=204)
def delete_NewsItems(id: int, db: Session = Depends(get_db)):
    NewsItems = crud.get_NewsItems(db=db, id=id)
    if NewsItems is None:
        raise HTTPException(status_code=404, detail="NewsItems not found")
    crud.delete_NewsItems(db=db, id=id)
          



#get news item by link
@app.get("/NewsItems/link/{link}", response_model=schemas.NewsItems)
def read_NewsItems_by_link(link: str, db: Session = Depends(get_db)):
    NewsItems = crud.get_NewsItems_by_link(db=db, link=link)
    if NewsItems is None:
        raise HTTPException(status_code=404, detail="NewsItems not found")
    return NewsItems


#put news item by link
@app.put("/NewsItems/link/{link}", response_model=schemas.NewsItems)
def update_NewsItems_by_link(link: str, NewsItems: schemas.NewsItemsUpdate, db: Session = Depends(get_db)):
    NewsItems_link = crud.get_NewsItems_by_link(db=db, link=link)
    if NewsItems_link is None:
        raise HTTPException(status_code=404, detail="NewsItems not found")
    return crud.update_NewsItems(db=db, id=NewsItems_link.id, NewsItems=NewsItems)


#delete news item by link
@app.delete("/NewsItems/link/{link}", status_code=204)
def delete_NewsItems_by_link(link: str, db: Session = Depends(get_db)):
    NewsItems = crud.get_NewsItems_by_link(db=db, link=link)
    if NewsItems is None:
        raise HTTPException(status_code=404, detail="NewsItems not found")
    crud.delete_NewsItems(db=db, id=NewsItems.id)


#get all news items by link
@app.get("/NewsItems/link", response_model=List[schemas.NewsItems])
def read_all_NewsItems_by_link(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    NewsItems = crud.get_all_NewsItems_by_link(db=db, skip=skip, limit=limit)
    return NewsItems


#get all news item by subtheme 
@app.get("/NewsItems/subtheme/{subtheme}", response_model=List[schemas.NewsItems])
def read_all_NewsItems_by_subtheme(subtheme: str, skip: int = 0, limit: int = 10000, db: Session = Depends(get_db)):
    NewsItems = crud.get_all_NewsItems_by_subtheme(db=db, subtheme=subtheme, skip=skip, limit=limit)
    return NewsItems


#delete all news item by subtheme
@app.delete("/NewsItems/subtheme/{subtheme}", status_code=204)
def delete_all_NewsItems_by_subtheme(subtheme: str, db: Session = Depends(get_db)):
    NewsItems = crud.get_all_NewsItems_by_subtheme(db=db, subtheme=subtheme)
    if NewsItems is None:
        raise HTTPException(status_code=404, detail="NewsItems not found")
    crud.delete_all_NewsItems_by_subtheme(db=db, subtheme=subtheme)    


#get all news item by theme
@app.get("/NewsItems/theme/{theme}", response_model=List[schemas.NewsItems])
def read_all_NewsItems_by_theme(theme: str, skip: int = 0, limit: int = 10000, db: Session = Depends(get_db)):
    NewsItems = crud.get_all_NewsItems_by_theme(db=db, theme=theme, skip=skip, limit=limit)
    return NewsItems


#delete all news item by theme
@app.delete("/NewsItems/theme/{theme}", status_code=204)
def delete_all_NewsItems_by_theme(theme: str, db: Session = Depends(get_db)):
    NewsItems = crud.get_all_NewsItems_by_theme(db=db, theme=theme)
    if NewsItems is None:
        raise HTTPException(status_code=404, detail="NewsItems not found")
    crud.delete_all_NewsItems_by_theme(db=db, theme=theme)
