from pydantic import BaseModel
from typing import Optional, List

# --- Users ---
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

# --- Auth ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# --- Orders ---
class OrderBase(BaseModel):
    service_type: str
    quantity: int
    amount_usd: str
    instagram_target: str

class OrderCreate(OrderBase):
    pass

class OrderOut(OrderBase):
    id: int
    status: str

    class Config:
        from_attributes = True

# --- Reviews ---
class ReviewBase(BaseModel):
    rating: int
    comment: str

class ReviewCreate(ReviewBase):
    pass

class ReviewOut(ReviewBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

# --- Content ---
class ContentItem(BaseModel):
    key: str
    value: str

    class Config:
        from_attributes = True

# --- Settings ---
class SettingItem(BaseModel):
    key: str
    value: str

    class Config:
        from_attributes = True
