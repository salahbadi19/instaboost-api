# routers/reviews.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import database, models, schemas

router = APIRouter(prefix="/api/reviews", tags=["reviews"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.ReviewOut)
def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    if not (1 <= review.rating <= 5):
        raise HTTPException(status_code=400, detail="التقييم يجب أن يكون بين 1 و 5")
    new_review = models.Review(
        user_id=1,
        rating=review.rating,
        comment=review.comment
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

@router.get("/", response_model=list[schemas.ReviewOut])
def get_reviews(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    reviews = db.query(models.Review).offset(skip).limit(limit).all()
    return reviews
