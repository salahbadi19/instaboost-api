# routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import database, models, schemas, auth

router = APIRouter(prefix="/api/users", tags=["users"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(db: Session = Depends(get_db), token: str = Depends(auth.oauth2_scheme)):
    # سيتم إضافته لاحقاً بعد دعم JWT الكامل
    # الآن نستخدم نموذج مبسط بدون مصادقة فعلية
    return {"id": 1, "username": "testuser"}

@router.put("/change-password")
def change_password(
    current_password: str,
    new_password: str,
    db: Session = Depends(get_db)
):
    # في الإنتاج: استخرج المستخدم من الـ token
    user = db.query(models.User).filter(models.User.id == 1).first()
    if not user or not auth.verify_password(current_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="كلمة المرور الحالية غير صحيحة")
    user.hashed_password = auth.get_password_hash(new_password)
    db.commit()
    return {"message": "تم تغيير كلمة المرور بنجاح"}

@router.put("/change-email")
def change_email(new_email: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == 1).first()
    existing = db.query(models.User).filter(models.User.email == new_email).first()
    if existing:
        raise HTTPException(status_code=400, detail="البريد الإلكتروني مستخدم مسبقاً")
    user.email = new_email
    db.commit()
    return {"message": "تم تحديث البريد الإلكتروني"}
