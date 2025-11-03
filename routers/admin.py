# routers/admin.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import database, models, schemas

router = APIRouter(prefix="/api/admin", tags=["admin"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/dashboard")
def admin_dashboard(db: Session = Depends(get_db)):
    total_users = db.query(models.User).count()
    today_orders = db.query(models.Order).filter(models.Order.status == "pending").count()
    total_reviews = db.query(models.Review).count()
    revenue = sum([float(o.amount_usd) for o in db.query(models.Order).filter(models.Order.status == "completed").all()])
    return {
        "total_users": total_users,
        "today_orders": today_orders,
        "total_reviews": total_reviews,
        "revenue_usd": round(revenue, 2)
    }

@router.get("/users", response_model=list[schemas.UserOut])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@router.get("/orders", response_model=list[schemas.OrderOut])
def get_all_orders(db: Session = Depends(get_db)):
    return db.query(models.Order).all()

@router.put("/orders/{order_id}/complete")
def complete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="الطلب غير موجود")
    order.status = "completed"
    db.commit()
    return {"message": "تم إكمال الطلب"}

@router.put("/orders/{order_id}/cancel")
def cancel_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="الطلب غير موجود")
    order.status = "cancelled"
    db.commit()
    return {"message": "تم إلغاء الطلب"}
