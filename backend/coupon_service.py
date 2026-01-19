from datetime import datetime
from typing import Optional
from schemas import CouponSchema, CouponApplySchema

async def validate_coupon(coupon_code: str, cart_total: float, coupons_collection) -> dict:
    """Validate and apply coupon code"""
    coupon = await coupons_collection.find_one({"code": coupon_code.upper()})
    
    if not coupon:
        return {"valid": False, "message": "Invalid coupon code"}
    
    if not coupon.get("is_active", True):
        return {"valid": False, "message": "Coupon is not active"}
    
    now = datetime.now()
    valid_from = coupon.get("valid_from")
    valid_until = coupon.get("valid_until")
    
    if valid_from and datetime.fromisoformat(str(valid_from)) > now:
        return {"valid": False, "message": "Coupon not yet valid"}
    
    if valid_until and datetime.fromisoformat(str(valid_until)) < now:
        return {"valid": False, "message": "Coupon has expired"}
    
    min_purchase = coupon.get("min_purchase")
    if min_purchase and cart_total < min_purchase:
        return {"valid": False, "message": f"Minimum purchase of ₹{min_purchase} required"}
    
    usage_limit = coupon.get("usage_limit")
    used_count = coupon.get("used_count", 0)
    if usage_limit and used_count >= usage_limit:
        return {"valid": False, "message": "Coupon usage limit reached"}
    
    # Calculate discount
    discount_type = coupon.get("discount_type", "percentage")
    discount_value = coupon.get("discount_value", 0)
    
    if discount_type == "percentage":
        discount_amount = (cart_total * discount_value) / 100
        max_discount = coupon.get("max_discount")
        if max_discount and discount_amount > max_discount:
            discount_amount = max_discount
    else:
        discount_amount = discount_value
        if discount_amount > cart_total:
            discount_amount = cart_total
    
    return {
        "valid": True,
        "discount_amount": round(discount_amount, 2),
        "discount_type": discount_type,
        "discount_value": discount_value,
        "final_amount": round(cart_total - discount_amount, 2),
        "coupon_id": str(coupon["_id"])
    }

async def apply_coupon(coupon_code: str, cart_total: float, coupons_collection) -> dict:
    """Apply coupon and increment usage count"""
    validation = await validate_coupon(coupon_code, cart_total, coupons_collection)
    
    if validation["valid"]:
        await coupons_collection.update_one(
            {"code": coupon_code.upper()},
            {"$inc": {"used_count": 1}}
        )
    
    return validation

