from fastapi import APIRouter, HTTPException, Request, Body, status, Depends
from app.schemas.orders import OrderCreate, OrderSchema
from app.routes.auth import get_current_user, get_current_admin_user
from app.services.email_service import send_order_confirmation, send_shipping_notification
from app.services.stripe_service import create_checkout_session
from typing import List, Optional
from bson import ObjectId
import os
from jose import jwt
from datetime import datetime

from app.auth import SECRET_KEY, ALGORITHM
from jose import jwt

router = APIRouter()

async def get_optional_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None: return None
        user = await request.app.mongodb["users"].find_one({"email": email})
        if user: user["_id"] = str(user["_id"])
        return user
    except:
        return None

@router.post("/", response_description="Place a new order", status_code=status.HTTP_201_CREATED)
async def create_order(
    request: Request, 
    order: OrderCreate = Body(...), 
    current_user: Optional[dict] = Depends(get_optional_user)
):
    order_dict = order.dict()
    
    # Handle User vs Guest
    if current_user:
        order_dict["user_id"] = str(current_user["_id"])
        user_email = current_user["email"]
    else:
        order_dict["user_id"] = "guest"
        user_email = order_dict.get("shipping_address", {}).get("email")
    
    if not user_email:
        raise HTTPException(status_code=400, detail="Customer email is required for the order")

    # Add timestamp
    order_dict["created_at"] = datetime.utcnow()
    
    new_order = await request.app.mongodb["orders"].insert_one(order_dict)
    created_order = await request.app.mongodb["orders"].find_one({"_id": new_order.inserted_id})
    created_order["_id"] = str(created_order["_id"])
    
    # Send Confirmation Email 
    send_order_confirmation(created_order, user_email)
    
    # Generate Stripe URL (if items present)
    try:
        # Convert "₹4,500" or similar to a number for Stripe
        numeric_total_str = "".join(filter(str.isdigit, str(order_dict["total_amount"])))
        if numeric_total_str:
            numeric_total = int(numeric_total_str)
            # Create Stripe session
            checkout_url = create_checkout_session(created_order["_id"], numeric_total, user_email)
            if checkout_url:
                return {"_id": created_order["_id"], "checkout_url": checkout_url}
    except Exception as e:
        print(f"Stripe Checkout Session Generation Failed: {e}")

    return created_order

@router.get("/my-orders", response_description="List my orders")
async def list_my_orders(request: Request, current_user: dict = Depends(get_current_user)):
    orders = []
    cursor = request.app.mongodb["orders"].find({"user_id": str(current_user["_id"])})
    async for order in cursor:
        order["_id"] = str(order["_id"])
        orders.append(order)
    return orders

@router.get("/all", response_description="List all orders (Admin only)")
async def list_all_orders(request: Request, admin: dict = Depends(get_current_admin_user)):
    orders = []
    cursor = request.app.mongodb["orders"].find()
    async for order in cursor:
        order["_id"] = str(order["_id"])
        orders.append(order)
    return orders

@router.put("/{id}/status", response_description="Update order status (Admin only)")
async def update_order_status(
    request: Request, 
    id: str, 
    order_status: str, 
    tracking_id: Optional[str] = None,
    tracking_url: Optional[str] = None,
    admin: dict = Depends(get_current_admin_user)
):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    update_data = {"order_status": order_status}
    if tracking_id: update_data["tracking_id"] = tracking_id
    if tracking_url: update_data["tracking_url"] = tracking_url

    update_result = await request.app.mongodb["orders"].update_one(
        {"_id": ObjectId(id)}, {"$set": update_data}
    )

    if update_result.modified_count == 1:
        # If shipped, send notification
        if order_status.lower() in ["shipped", "delivered"]:
            order = await request.app.mongodb["orders"].find_one({"_id": ObjectId(id)})
            
            # Determine email (User email or shipping email for guest)
            customer_email = order.get("shipping_address", {}).get("email")
            if order.get("user_id") != "guest" and ObjectId.is_valid(order["user_id"]):
                user = await request.app.mongodb["users"].find_one({"_id": ObjectId(order["user_id"])})
                if user:
                    customer_email = user["email"]
            
            if customer_email:
                send_shipping_notification(id, customer_email, tracking_id or "N/A", tracking_url or "#")
        return {"message": "Order status updated successfully"}
    
    raise HTTPException(status_code=404, detail=f"Order {id} not found")
