# routers/orders.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import database, models, schemas

router = APIRouter(prefix="/api/orders", tags=["orders"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/free-trial", response_model=schemas.OrderOut)
def create_free_trial(
    instagram_target: str,
    db: Session = Depends(get_db)
):
    # التحقق من أن المستخدم لم يطلب الخطة المجانية من قبل
    existing = db.query(models.Order).filter(
        models.Order.user_id == 1,
        models.Order.status == "completed",
        models.Order.quantity == 20
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="لقد استخدمت الخطة المجانية مسبقاً")

    new_order = models.Order(
        user_id=1,
        service_type="followers_likes",
        quantity=20,
        amount_usd="0.00",
        instagram_target=instagram_target,
        status="pending"
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

@router.post("/paid", response_model=schemas.OrderOut)
def create_paid_order(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db)
):
    # التحقق من صحة الكمية والسعر (مثال: 100 متابع = $0.2)
    if order.service_type == "followers" and order.quantity >= 100:
        expected_price = f"{order.quantity / 100 * 0.2:.2f}"
    elif order.service_type == "likes" and order.quantity >= 100:
        expected_price = f"{order.quantity / 100 * 0.1:.2f}"
    else:
        raise HTTPException(status_code=400, detail="الكمية غير مدعومة أو أقل من الحد الأدنى")

    if order.amount_usd != expected_price:
        raise HTTPException(status_code=400, detail="السعر غير صحيح")

    new_order = models.Order(
        user_id=1,
        service_type=order.service_type,
        quantity=order.quantity,
        amount_usd=order.amount_usd,
        instagram_target=order.instagram_target,
        status="pending"
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order
