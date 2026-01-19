from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")

client = AsyncIOMotorClient(MONGO_URL)
db = client["ecommerce_db"]

# Collections
users = db.users
products = db.products
orders = db.orders
addresses = db.addresses
cart = db.cart
coupons = db.coupons
payments = db.payments
shipping_trackers = db.shipping_trackers
categories = db.categories
reviews = db.reviews

# Create indexes for better performance
async def create_indexes():
    """Create database indexes for better query performance"""
    await users.create_index("email", unique=True)
    await products.create_index("category")
    await products.create_index("name")
    await products.create_index([("name", "text"), ("description", "text")])
    await orders.create_index("user_email")
    await orders.create_index("tracking_number")
    await orders.create_index("status")
    await addresses.create_index("user_email")
    await cart.create_index("user_email")
    await coupons.create_index("code", unique=True)
    await payments.create_index("order_id")
    await shipping_trackers.create_index("tracking_number", unique=True)
    await shipping_trackers.create_index("order_id")
