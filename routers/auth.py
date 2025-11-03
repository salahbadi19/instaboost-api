# routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from .. import database, models, schemas, auth  # تأكد من أن المسار صحيح حسب بنية المشروع

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)

# ✅ تعريف الـ OAuth2Scheme حتى يمكن استخدامه في ملفات أخرى مثل users.py
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# -----------------------------
# دالة لجلب جلسة قاعدة البيانات
# -----------------------------
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------------
# تسجيل مستخدم جديد
# -----------------------------
@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # تحقق من أن المستخدم غير موجود مسبقًا
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="اسم المستخدم مسجل مسبقاً")

    # تشفير كلمة المرور
    hashed_pw = auth.get_password_hash(user.password)
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pw,
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# -----------------------------
# تسجيل الدخول (JWT)
# -----------------------------
@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # التحقق من وجود المستخدم
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="اسم المستخدم أو كلمة المرور غير صحيحة",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # إنشاء توكن JWT
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
