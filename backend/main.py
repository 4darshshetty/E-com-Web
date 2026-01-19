from fastapi import FastAPI, HTTPException
from database import users, products, orders
from schemas import *
from auth import *

import ctypes

app = FastAPI()

# ---------- LOAD C++ DISCOUNT ENGINE ----------
discount = ctypes.CDLL("../cpp-engine/discount.so")
discount.applyDiscount.restype = ctypes.c_double

def apply_discount(price, percent):
    return discount.applyDiscount(
        ctypes.c_double(price),
        ctypes.c_int(percent)
    )

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
async def add_product(p: ProductSchema):
    await products.insert_one(p.dict())
    return {"msg": "Product added"}

@app.get("/products")
async def get_products():
    result = []
    async for p in products.find():
        p["_id"] = str(p["_id"])
        result.append(p)
    return result

# ---------- ORDERS ----------
@app.post("/order")
async def place_order(order: OrderSchema, coupon: int = 0):
    order.total = apply_discount(order.total, coupon)
    await orders.insert_one(order.dict())
    return {"final_price": order.total}

@app.get("/track/{email}")
async def track(email: str):
    result = []
    async for o in orders.find({"user_email": email}):
        o["_id"] = str(o["_id"])
        result.append(o)
    return result
