# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, users, orders, reviews, content, admin, chat
from database import engine
import models

# إنشاء جداول قاعدة البيانات تلقائيًا عند التشغيل
models.Base.metadata.create_all(bind=engine)

# إنشاء تطبيق FastAPI
app = FastAPI(title="InstaBoost API")

# تمكين CORS (للسماح للواجهة الأمامية بالتواصل مع الـ API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # في الإنتاج: غيّرها إلى نطاق موقعك الحقيقي (مثل: ["https://yourdomain.com"])
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# تضمين جميع الـ routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(orders.router)
app.include_router(reviews.router)
app.include_router(content.router)
app.include_router(admin.router)
app.include_router(chat.router)  # دردشة الدعم عبر WebSocket

# نقطة جذر بسيطة للاختبار
@app.get("/")
def root():
    return {"message": "🚀 InstaBoost API is running successfully!"}
