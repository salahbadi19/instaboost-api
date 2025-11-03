# routers/content.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import database, models, schemas

router = APIRouter(prefix="/api/content", tags=["content"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.ContentItem])
def get_all_content(db: Session = Depends(get_db)):
    return db.query(models.Content).all()

@router.put("/{key}", response_model=schemas.ContentItem)
def update_content(key: str, item: schemas.ContentItem, db: Session = Depends(get_db)):
    content = db.query(models.Content).filter(models.Content.key == key).first()
    if not content:
        content = models.Content(key=key, value=item.value)
        db.add(content)
    else:
        content.value = item.value
    db.commit()
    db.refresh(content)
    return content
