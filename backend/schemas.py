from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class OrderStatus(str, Enum):
    PENDING = "Pending"
    PROCESSING = "Processing"
    CONFIRMED = "Confirmed"
    SHIPPED = "Shipped"
    IN_TRANSIT = "In Transit"
    OUT_FOR_DELIVERY = "Out for Delivery"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"

class PaymentStatus(str, Enum):
    PENDING = "Pending"
    PROCESSING = "Processing"
    COMPLETED = "Completed"
    FAILED = "Failed"
    REFUNDED = "Refunded"

class PaymentMethod(str, Enum):
    CREDIT_CARD = "Credit Card"
    DEBIT_CARD = "Debit Card"
    PAYPAL = "PayPal"
    BANK_TRANSFER = "Bank Transfer"
    UPI = "UPI"

# User Schemas
class UserSchema(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    phone: Optional[str] = None
    role: UserRole = UserRole.USER

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserUpdateSchema(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None

# Address Schemas
class AddressSchema(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str
    country: str = "India"
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_default: bool = False

class AddressResponseSchema(BaseModel):
    id: str
    street: str
    city: str
    state: str
    zip_code: str
    country: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_default: bool

# Product Schemas
class ProductSchema(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    original_price: Optional[float] = None
    category: str
    subcategory: Optional[str] = None
    brand: Optional[str] = None
    stock: int
    images: List[str] = []
    specifications: dict = {}
    rating: float = 0.0
    reviews_count: int = 0
    is_featured: bool = False
    is_active: bool = True

class ProductUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    original_price: Optional[float] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    brand: Optional[str] = None
    stock: Optional[int] = None
    images: Optional[List[str]] = None
    specifications: Optional[dict] = None
    is_featured: Optional[bool] = None
    is_active: Optional[bool] = None

# Cart Schemas
class CartItemSchema(BaseModel):
    product_id: str
    quantity: int
    price: float

class CartSchema(BaseModel):
    items: List[CartItemSchema] = []
    total: float = 0.0
    discount: float = 0.0
    final_total: float = 0.0

# Coupon Schemas
class CouponSchema(BaseModel):
    code: str
    discount_type: str  # "percentage" or "fixed"
    discount_value: float
    min_purchase: Optional[float] = None
    max_discount: Optional[float] = None
    valid_from: datetime
    valid_until: datetime
    usage_limit: Optional[int] = None
    used_count: int = 0
    is_active: bool = True

class CouponApplySchema(BaseModel):
    code: str
    cart_total: float

# Order Schemas
class OrderItemSchema(BaseModel):
    product_id: str
    product_name: str
    quantity: int
    price: float
    total: float

class OrderSchema(BaseModel):
    user_email: str
    items: List[OrderItemSchema]
    shipping_address: AddressSchema
    billing_address: Optional[AddressSchema] = None
    subtotal: float
    shipping_cost: float = 0.0
    discount: float = 0.0
    tax: float = 0.0
    total: float
    coupon_code: Optional[str] = None
    payment_method: PaymentMethod
    payment_status: PaymentStatus = PaymentStatus.PENDING
    status: OrderStatus = OrderStatus.PENDING
    tracking_number: Optional[str] = None
    notes: Optional[str] = None

class OrderUpdateSchema(BaseModel):
    status: Optional[OrderStatus] = None
    payment_status: Optional[PaymentStatus] = None
    tracking_number: Optional[str] = None
    notes: Optional[str] = None

# Shipping Tracker Schemas
class ShippingLocationSchema(BaseModel):
    latitude: float
    longitude: float
    address: str
    timestamp: datetime
    status: str
    description: Optional[str] = None

class ShippingTrackerSchema(BaseModel):
    order_id: str
    tracking_number: str
    current_location: ShippingLocationSchema
    history: List[ShippingLocationSchema] = []
    estimated_delivery: Optional[datetime] = None

# Payment Schemas
class PaymentSchema(BaseModel):
    order_id: str
    amount: float
    payment_method: PaymentMethod
    transaction_id: Optional[str] = None
    payment_status: PaymentStatus = PaymentStatus.PENDING

class PaymentIntentSchema(BaseModel):
    amount: float
    currency: str = "INR"
    payment_method: PaymentMethod

# Admin Analytics Schemas
class SalesStatsSchema(BaseModel):
    total_revenue: float
    total_orders: int
    total_users: int
    total_products: int
    revenue_by_category: dict
    revenue_by_month: List[dict]
    top_products: List[dict]
    recent_orders: List[dict]

class PaymentStatsSchema(BaseModel):
    total_received: float
    pending_payments: float
    failed_payments: float
    refunded_amount: float
    payments_by_method: dict
    payments_by_date: List[dict]
