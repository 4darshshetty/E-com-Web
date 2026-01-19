from fastapi import FastAPI, HTTPException, Depends, Header, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import (
    users, products, orders, addresses, cart, coupons, 
    payments, shipping_trackers, categories, reviews, create_indexes
)
from schemas import *
from auth import *
import os
import sys
from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from enum import Enum

try:
    from payment import create_payment_intent, confirm_payment, mock_payment
    STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "sk_test_your_stripe_secret_key")
except ImportError:
    def mock_payment(amount, method):
        return {"transaction_id": f"mock_{hash(str(amount))}", "status": "completed", "amount": amount}
    def create_payment_intent(amount, currency, metadata):
        return {"client_secret": None, "payment_intent_id": f"mock_{hash(str(amount))}", "status": "requires_payment_method"}
    def confirm_payment(intent_id):
        return {"status": "completed", "amount": 0, "currency": "INR"}
    STRIPE_SECRET_KEY = "sk_test_mock"
from shipping import (
    generate_tracking_number, calculate_shipping_cost, 
    calculate_distance, estimate_delivery_time, update_shipping_location
)
from coupon_service import validate_coupon, apply_coupon
from jose import jwt, JWTError

import ctypes

app = FastAPI(title="Advanced E-Commerce API", version="2.0.0")

# ---------- CORS ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- STARTUP ----------
@app.on_event("startup")
async def startup_event():
    await create_indexes()
    print("Database indexes created")

# ---------- LOAD C++ DISCOUNT ENGINE ----------
try:
    if sys.platform == "win32":
        dll_path = os.path.join(os.path.dirname(__file__), "..", "cpp-engine", "discount.dll")
        if os.path.exists(dll_path):
            discount = ctypes.CDLL(dll_path)
        else:
            discount = None
    else:
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
            return discount.applyDiscount(ctypes.c_double(price), ctypes.c_int(percent))
        except:
            pass
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

# ========== AUTH ENDPOINTS ==========
@app.post("/signup")
async def signup(user: UserSchema):
    if await users.find_one({"email": user.email}):
        raise HTTPException(400, "User exists")
    user_dict = user.dict()
    user_dict["password"] = hash_password(user_dict["password"])
    user_dict["created_at"] = datetime.now()
    await users.insert_one(user_dict)
    return {"msg": "Signup success"}

@app.post("/login")
async def login(data: LoginSchema):
    user = await users.find_one({"email": data.email})
    if not user or not verify_password(data.password, user["password"]):
        raise HTTPException(401, "Invalid login")
    token = create_token({
        "email": user["email"], 
        "role": user.get("role", "user"),
        "user_id": str(user["_id"])
    })
    return {"token": token, "user": {
        "email": user["email"],
        "role": user.get("role", "user"),
        "full_name": user.get("full_name")
    }}

@app.post("/logout")
async def logout(user: dict = Depends(get_current_user)):
    return {"msg": "Logged out successfully"}

# ========== USER PROFILE ENDPOINTS ==========
@app.get("/user/profile")
async def get_profile(user: dict = Depends(get_current_user)):
    user_data = await users.find_one({"email": user["email"]})
    if not user_data:
        raise HTTPException(404, "User not found")
    user_data["_id"] = str(user_data["_id"])
    user_data.pop("password", None)
    return user_data

@app.put("/user/profile")
async def update_profile(update: UserUpdateSchema, user: dict = Depends(get_current_user)):
    update_dict = {k: v for k, v in update.dict().items() if v is not None}
    if update_dict:
        await users.update_one({"email": user["email"]}, {"$set": update_dict})
    return {"msg": "Profile updated"}

# ========== ADDRESS ENDPOINTS ==========
@app.post("/user/addresses")
async def add_address(address: AddressSchema, user: dict = Depends(get_current_user)):
    address_dict = address.dict()
    address_dict["user_email"] = user["email"]
    address_dict["created_at"] = datetime.now()
    
    if address.is_default:
        await addresses.update_many(
            {"user_email": user["email"]},
            {"$set": {"is_default": False}}
        )
    
    result = await addresses.insert_one(address_dict)
    return {"id": str(result.inserted_id), "msg": "Address added"}

@app.get("/user/addresses")
async def get_addresses(user: dict = Depends(get_current_user)):
    result = []
    async for addr in addresses.find({"user_email": user["email"]}):
        addr["_id"] = str(addr["_id"])
        result.append(addr)
    return result

@app.delete("/user/addresses/{address_id}")
async def delete_address(address_id: str, user: dict = Depends(get_current_user)):
    result = await addresses.delete_one({
        "_id": ObjectId(address_id),
        "user_email": user["email"]
    })
    if result.deleted_count == 0:
        raise HTTPException(404, "Address not found")
    return {"msg": "Address deleted"}

# ========== PRODUCT ENDPOINTS ==========
@app.post("/products")
async def add_product(p: ProductSchema, admin: dict = Depends(get_admin_user)):
    product_dict = p.dict()
    product_dict["created_at"] = datetime.now()
    result = await products.insert_one(product_dict)
    return {"id": str(result.inserted_id), "msg": "Product added"}

@app.get("/products")
async def get_products(
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    featured: Optional[bool] = Query(None),
    user: dict = Depends(get_current_user)
):
    query = {"is_active": True}
    if category:
        query["category"] = category
    if featured is not None:
        query["is_featured"] = featured
    if min_price or max_price:
        price_query = {}
        if min_price:
            price_query["$gte"] = min_price
        if max_price:
            price_query["$lte"] = max_price
        query["price"] = price_query
    
    result = []
    async for p in products.find(query):
        p["_id"] = str(p["_id"])
        if search and search.lower() not in p.get("name", "").lower():
            continue
        result.append(p)
    return result

@app.get("/products/{product_id}")
async def get_product(product_id: str, user: dict = Depends(get_current_user)):
    product = await products.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(404, "Product not found")
    product["_id"] = str(product["_id"])
    return product

@app.put("/products/{product_id}")
async def update_product(
    product_id: str, 
    update: ProductUpdateSchema, 
    admin: dict = Depends(get_admin_user)
):
    update_dict = {k: v for k, v in update.dict().items() if v is not None}
    if update_dict:
        await products.update_one({"_id": ObjectId(product_id)}, {"$set": update_dict})
    return {"msg": "Product updated"}

@app.delete("/products/{product_id}")
async def delete_product(product_id: str, admin: dict = Depends(get_admin_user)):
    await products.update_one({"_id": ObjectId(product_id)}, {"$set": {"is_active": False}})
    return {"msg": "Product deleted"}

@app.get("/products/categories/list")
async def get_categories(user: dict = Depends(get_current_user)):
    categories_list = await products.distinct("category")
    return {"categories": categories_list}

# ========== CART ENDPOINTS ==========
@app.post("/cart/add")
async def add_to_cart(item: CartItemSchema, user: dict = Depends(get_current_user)):
    product = await products.find_one({"_id": ObjectId(item.product_id)})
    if not product:
        raise HTTPException(404, "Product not found")
    
    cart_item = {
        "user_email": user["email"],
        "product_id": item.product_id,
        "quantity": item.quantity,
        "price": item.price,
        "added_at": datetime.now()
    }
    
    await cart.update_one(
        {"user_email": user["email"], "product_id": item.product_id},
        {"$set": cart_item},
        upsert=True
    )
    return {"msg": "Item added to cart"}

@app.get("/cart")
async def get_cart(user: dict = Depends(get_current_user)):
    cart_items = []
    total = 0.0
    
    async for item in cart.find({"user_email": user["email"]}):
        product = await products.find_one({"_id": ObjectId(item["product_id"])})
        if product:
            item_total = item["quantity"] * item["price"]
            total += item_total
            cart_items.append({
                "id": str(item["_id"]),
                "product": {
                    "id": str(product["_id"]),
                    "name": product["name"],
                    "price": product["price"],
                    "images": product.get("images", [])
                },
                "quantity": item["quantity"],
                "total": item_total
            })
    
    return {"items": cart_items, "total": round(total, 2)}

@app.delete("/cart/{item_id}")
async def remove_from_cart(item_id: str, user: dict = Depends(get_current_user)):
    result = await cart.delete_one({"_id": ObjectId(item_id), "user_email": user["email"]})
    if result.deleted_count == 0:
        raise HTTPException(404, "Item not found")
    return {"msg": "Item removed from cart"}

@app.delete("/cart")
async def clear_cart(user: dict = Depends(get_current_user)):
    await cart.delete_many({"user_email": user["email"]})
    return {"msg": "Cart cleared"}

# ========== COUPON ENDPOINTS ==========
@app.post("/coupons")
async def create_coupon(coupon: CouponSchema, admin: dict = Depends(get_admin_user)):
    coupon_dict = coupon.dict()
    coupon_dict["code"] = coupon_dict["code"].upper()
    coupon_dict["created_at"] = datetime.now()
    
    if await coupons.find_one({"code": coupon_dict["code"]}):
        raise HTTPException(400, "Coupon code already exists")
    
    result = await coupons.insert_one(coupon_dict)
    return {"id": str(result.inserted_id), "msg": "Coupon created"}

@app.post("/coupons/validate")
async def validate_coupon_code(
    coupon_data: CouponApplySchema, 
    user: dict = Depends(get_current_user)
):
    result = await validate_coupon(coupon_data.code, coupon_data.cart_total, coupons)
    return result

@app.get("/coupons")
async def get_coupons(admin: dict = Depends(get_admin_user)):
    result = []
    async for c in coupons.find({"is_active": True}):
        c["_id"] = str(c["_id"])
        result.append(c)
    return result

# ========== ORDER ENDPOINTS ==========
@app.post("/orders")
async def create_order(order: OrderSchema, user: dict = Depends(get_current_user)):
    if order.user_email != user["email"]:
        raise HTTPException(403, "Cannot create order for another user")
    
    # Apply coupon if provided
    discount_amount = 0.0
    if order.coupon_code:
        coupon_result = await apply_coupon(order.coupon_code, order.subtotal, coupons)
        if coupon_result["valid"]:
            discount_amount = coupon_result["discount_amount"]
    
    # Calculate final total
    final_total = order.subtotal + order.shipping_cost + order.tax - discount_amount
    
    order_dict = order.dict()
    order_dict["total"] = final_total
    order_dict["discount"] = discount_amount
    order_dict["created_at"] = datetime.now()
    
    # Generate tracking number
    tracking_number = generate_tracking_number()
    order_dict["tracking_number"] = tracking_number
    
    # Create order
    result = await orders.insert_one(order_dict)
    order_id = str(result.inserted_id)
    
    # Create shipping tracker
    shipping_location = {
        "order_id": order_id,
        "tracking_number": tracking_number,
        "current_location": {
            "latitude": order.shipping_address.latitude or 0.0,
            "longitude": order.shipping_address.longitude or 0.0,
            "address": f"{order.shipping_address.street}, {order.shipping_address.city}",
            "timestamp": datetime.now(),
            "status": order.status.value,
            "description": "Order placed"
        },
        "history": [],
        "estimated_delivery": estimate_delivery_time(100)  # Default distance
    }
    await shipping_trackers.insert_one(shipping_location)
    
    # Clear cart
    await cart.delete_many({"user_email": user["email"]})
    
    return {
        "order_id": order_id,
        "tracking_number": tracking_number,
        "total": final_total,
        "msg": "Order created successfully"
    }

@app.get("/orders")
async def get_orders(user: dict = Depends(get_current_user)):
    query = {"user_email": user["email"]}
    if user.get("role") == "admin":
        query = {}  # Admin can see all orders
    
    result = []
    async for o in orders.find(query).sort("created_at", -1):
        o["_id"] = str(o["_id"])
        result.append(o)
    return result

@app.get("/orders/{order_id}")
async def get_order(order_id: str, user: dict = Depends(get_current_user)):
    query = {"_id": ObjectId(order_id)}
    if user.get("role") != "admin":
        query["user_email"] = user["email"]
    
    order = await orders.find_one(query)
    if not order:
        raise HTTPException(404, "Order not found")
    order["_id"] = str(order["_id"])
    return order

@app.put("/orders/{order_id}")
async def update_order(
    order_id: str,
    update: OrderUpdateSchema,
    admin: dict = Depends(get_admin_user)
):
    update_dict = {k: v.value if isinstance(v, Enum) else v 
                   for k, v in update.dict().items() if v is not None}
    
    if update_dict:
        await orders.update_one({"_id": ObjectId(order_id)}, {"$set": update_dict})
        
        # Update shipping tracker if status changed
        if "status" in update_dict:
            tracker = await shipping_trackers.find_one({"order_id": order_id})
            if tracker:
                new_location = {
                    "latitude": tracker["current_location"]["latitude"],
                    "longitude": tracker["current_location"]["longitude"],
                    "address": tracker["current_location"]["address"],
                    "timestamp": datetime.now(),
                    "status": update_dict["status"],
                    "description": f"Status updated to {update_dict['status']}"
                }
                await shipping_trackers.update_one(
                    {"order_id": order_id},
                    {
                        "$set": {"current_location": new_location},
                        "$push": {"history": new_location}
                    }
                )
    
    return {"msg": "Order updated"}

# ========== SHIPPING TRACKER ENDPOINTS ==========
@app.get("/track/{tracking_number}")
async def track_order(tracking_number: str, user: dict = Depends(get_current_user)):
    tracker = await shipping_trackers.find_one({"tracking_number": tracking_number})
    if not tracker:
        raise HTTPException(404, "Tracking number not found")
    
    # Verify user has access
    order = await orders.find_one({"tracking_number": tracking_number})
    if order and order["user_email"] != user["email"] and user.get("role") != "admin":
        raise HTTPException(403, "Access denied")
    
    tracker["_id"] = str(tracker["_id"])
    return tracker

@app.put("/track/{tracking_number}/location")
async def update_tracking_location(
    tracking_number: str,
    location: ShippingLocationSchema,
    admin: dict = Depends(get_admin_user)
):
    tracker = await shipping_trackers.find_one({"tracking_number": tracking_number})
    if not tracker:
        raise HTTPException(404, "Tracking number not found")
    
    location_dict = location.dict()
    location_dict["timestamp"] = datetime.now()
    
    await shipping_trackers.update_one(
        {"tracking_number": tracking_number},
        {
            "$set": {"current_location": location_dict},
            "$push": {"history": location_dict}
        }
    )
    
    # Update order status
    await orders.update_one(
        {"tracking_number": tracking_number},
        {"$set": {"status": location.status}}
    )
    
    return {"msg": "Location updated"}

# ========== PAYMENT ENDPOINTS ==========
@app.post("/payments/intent")
async def create_payment_intent_endpoint(
    payment_data: PaymentIntentSchema,
    user: dict = Depends(get_current_user)
):
    try:
        if STRIPE_SECRET_KEY.startswith("sk_test"):
            # Use mock payment for development
            result = mock_payment(payment_data.amount, payment_data.payment_method.value)
            return {
                "client_secret": None,
                "payment_intent_id": result["transaction_id"],
                "status": result["status"],
                "mock": True
            }
        else:
            result = create_payment_intent(
                payment_data.amount,
                payment_data.currency,
                {"user_email": user["email"]}
            )
            return result
    except Exception as e:
        raise HTTPException(400, str(e))

@app.post("/payments/confirm")
async def confirm_payment_endpoint(
    payment_intent_id: str,
    order_id: str,
    user: dict = Depends(get_current_user)
):
    try:
        if STRIPE_SECRET_KEY.startswith("sk_test"):
            payment_status = {"status": "completed", "amount": 0}
        else:
            payment_status = confirm_payment(payment_intent_id)
        
        # Save payment record
        payment_record = {
            "order_id": order_id,
            "user_email": user["email"],
            "amount": payment_status["amount"],
            "payment_intent_id": payment_intent_id,
            "status": payment_status["status"],
            "created_at": datetime.now()
        }
        await payments.insert_one(payment_record)
        
        # Update order payment status
        await orders.update_one(
            {"_id": ObjectId(order_id)},
            {"$set": {"payment_status": PaymentStatus.COMPLETED}}
        )
        
        return {"msg": "Payment confirmed", "status": payment_status["status"]}
    except Exception as e:
        raise HTTPException(400, str(e))

# ========== ADMIN ANALYTICS ENDPOINTS ==========
@app.get("/admin/analytics/sales")
async def get_sales_stats(admin: dict = Depends(get_admin_user)):
    total_revenue = 0.0
    total_orders = await orders.count_documents({})
    total_users = await users.count_documents({})
    total_products = await products.count_documents({"is_active": True})
    
    revenue_by_category = {}
    revenue_by_month = {}
    
    async for order in orders.find({"payment_status": "Completed"}):
        total_revenue += order.get("total", 0)
        
        # Revenue by category
        for item in order.get("items", []):
            product = await products.find_one({"_id": ObjectId(item["product_id"])})
            if product:
                category = product.get("category", "Other")
                revenue_by_category[category] = revenue_by_category.get(category, 0) + item["total"]
        
        # Revenue by month
        month_key = order.get("created_at", datetime.now()).strftime("%Y-%m")
        revenue_by_month[month_key] = revenue_by_month.get(month_key, 0) + order.get("total", 0)
    
    # Get top products
    product_sales = {}
    async for order in orders.find():
        for item in order.get("items", []):
            product_id = item["product_id"]
            product_sales[product_id] = product_sales.get(product_id, 0) + item["quantity"]
    
    top_products = []
    for product_id, quantity in sorted(product_sales.items(), key=lambda x: x[1], reverse=True)[:10]:
        product = await products.find_one({"_id": ObjectId(product_id)})
        if product:
            top_products.append({
                "id": str(product["_id"]),
                "name": product["name"],
                "sales": quantity
            })
    
    # Recent orders
    recent_orders = []
    async for order in orders.find().sort("created_at", -1).limit(10):
        order["_id"] = str(order["_id"])
        recent_orders.append(order)
    
    return {
        "total_revenue": round(total_revenue, 2),
        "total_orders": total_orders,
        "total_users": total_users,
        "total_products": total_products,
        "revenue_by_category": revenue_by_category,
        "revenue_by_month": [{"month": k, "revenue": v} for k, v in revenue_by_month.items()],
        "top_products": top_products,
        "recent_orders": recent_orders
    }

@app.get("/admin/analytics/payments")
async def get_payment_stats(admin: dict = Depends(get_admin_user)):
    total_received = 0.0
    pending_payments = 0.0
    failed_payments = 0.0
    refunded_amount = 0.0
    payments_by_method = {}
    payments_by_date = {}
    
    async for payment in payments.find():
        amount = payment.get("amount", 0)
        status = payment.get("status", "pending")
        method = payment.get("payment_method", "Unknown")
        
        if status == "completed":
            total_received += amount
        elif status == "pending":
            pending_payments += amount
        elif status == "failed":
            failed_payments += amount
        elif status == "refunded":
            refunded_amount += amount
        
        payments_by_method[method] = payments_by_method.get(method, 0) + amount
        
        date_key = payment.get("created_at", datetime.now()).strftime("%Y-%m-%d")
        payments_by_date[date_key] = payments_by_date.get(date_key, 0) + amount
    
    return {
        "total_received": round(total_received, 2),
        "pending_payments": round(pending_payments, 2),
        "failed_payments": round(failed_payments, 2),
        "refunded_amount": round(refunded_amount, 2),
        "payments_by_method": payments_by_method,
        "payments_by_date": [{"date": k, "amount": v} for k, v in payments_by_date.items()]
    }

@app.get("/admin/orders/tracking")
async def get_all_tracking(admin: dict = Depends(get_admin_user)):
    result = []
    async for tracker in shipping_trackers.find():
        tracker["_id"] = str(tracker["_id"])
        result.append(tracker)
    return result

