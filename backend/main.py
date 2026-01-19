from fastapi import FastAPI, HTTPException, Depends, Header, Query
from fastapi.middleware.cors import CORSMiddleware
from database import users, products, orders
from schemas import *
from auth import *
from jose import jwt, JWTError

import ctypes
import os
import sys

app = FastAPI()

# ---------- CORS ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- LOAD C++ DISCOUNT ENGINE ----------
try:
    # Try Windows DLL first
    if sys.platform == "win32":
        dll_path = os.path.join(os.path.dirname(__file__), "..", "cpp-engine", "discount.dll")
        if os.path.exists(dll_path):
            discount = ctypes.CDLL(dll_path)
        else:
            # Fallback to Python implementation
            discount = None
    else:
        # Linux/Mac
        so_path = os.path.join(os.path.dirname(__file__), "..", "cpp-engine", "discount.so")
        if os.path.exists(so_path):
            discount = ctypes.CDLL(so_path)
        else:
            discount = None
    
    if discount:
        discount.applyDiscount.restype = ctypes.c_double
except Exception as e:
    print(f"Warning: Could not load C++ discount engine: {e}")
    discount = None

def apply_discount(price, percent):
    if discount:
        try:
            return discount.applyDiscount(
                ctypes.c_double(price),
                ctypes.c_int(percent)
            )
        except:
            pass
    # Python fallback
    if percent < 0 or percent > 70:
        return price
    return price - (price * percent / 100.0)

# ---------- AUTH DEPENDENCY ----------
async def get_current_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Not authenticated")
    
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        if email is None:
            raise HTTPException(401, "Invalid token")
        return payload
    except JWTError:
        raise HTTPException(401, "Invalid token")

async def get_admin_user(user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(403, "Admin access required")
    return user

# ---------- AUTH ----------
@app.post("/signup")
async def signup(user: UserSchema):
    if await users.find_one({"email": user.email}):
        raise HTTPException(400, "User exists")
    user.password = hash_password(user.password)
    await users.insert_one(user.dict())
    return {"msg": "Signup success"}

@app.post("/login")
async def login(data: LoginSchema):
    user = await users.find_one({"email": data.email})
    if not user or not verify_password(data.password, user["password"]):
        raise HTTPException(401, "Invalid login")
    token = create_token({"email": user["email"], "role": user["role"]})
    return {"token": token}

# ---------- PRODUCTS ----------
@app.post("/products")
async def add_product(p: ProductSchema, admin: dict = Depends(get_admin_user)):
    await products.insert_one(p.dict())
    return {"msg": "Product added"}

@app.get("/products")
async def get_products(user: dict = Depends(get_current_user)):
    result = []
    async for p in products.find():
        p["_id"] = str(p["_id"])
        result.append(p)
    return result

# ---------- ORDERS ----------
@app.post("/order")
async def place_order(order: OrderSchema, coupon: int = Query(0, ge=0, le=70), user: dict = Depends(get_current_user)):
    # Ensure user can only place orders for themselves
    if order.user_email != user.get("email"):
        raise HTTPException(403, "Cannot place order for another user")
    
    final_price = apply_discount(order.total, coupon)
    order_dict = order.dict()
    order_dict["total"] = final_price
    await orders.insert_one(order_dict)
    return {"final_price": final_price}

@app.get("/track/{email}")
async def track(email: str, user: dict = Depends(get_current_user)):
    # Ensure users can only track their own orders (unless admin)
    if email != user.get("email") and user.get("role") != "admin":
        raise HTTPException(403, "Cannot track orders for another user")
    
    result = []
    async for o in orders.find({"user_email": email}):
        o["_id"] = str(o["_id"])
        result.append(o)
    return result
