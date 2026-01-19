from pydantic import BaseModel
from typing import List, Optional

class UserSchema(BaseModel):
    email: str
    password: str
    role: str = "user"

class LoginSchema(BaseModel):
    email: str
    password: str

class ProductSchema(BaseModel):
    name: str
    price: float
    category: str
    stock: int

class OrderSchema(BaseModel):
    user_email: str
    products: List[str]
    total: float
    status: str = "Processing"
    location: Optional[str] = None
