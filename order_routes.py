from fastapi import APIRouter, HTTPException, Request, Body, status
from typing import List
from models import Order, OrderUpdate
from datetime import datetime
import requests
import httpx
router = APIRouter()

# POST /order - Create a new order
@router.post("/", response_description="Create a new order", status_code=status.HTTP_201_CREATED, response_model=Order)
async def create_order(request: Request, order: Order = Body(...)):
    # 1. Use httpx to make async requests
    async with httpx.AsyncClient() as client:
        # Query Product Service to get product details
        product_url = f"http://127.0.0.1:8000/product/{order.product_id}"
        product_response = await client.get(product_url)
        if product_response.status_code != 200:
            raise HTTPException(status_code=product_response.status_code, detail="Product not found")
        product_data = product_response.json()

        product_name = product_data.get("product_name")
        if not product_name:
            raise HTTPException(status_code=404, detail="Product name not found")
        order.product_ordered = product_name

        # Query Discount Service to get discount details
        discount_url = f"http://127.0.0.1:8000/discount/{order.product_id}"
        discount_response = await client.get(discount_url)
        if discount_response.status_code != 200:
            raise HTTPException(status_code=discount_response.status_code, detail="Discount not found")
        discount_data = discount_response.json()

    # Calculate total cost after discount
    discounted_price = float(discount_data['discounted_price'][1:].replace(',', ''))  # Remove ₹ and commas
    total_cost = discounted_price * order.quantity

    # 3. Add order to the database (mocked here for demonstration)
    order_data = order.dict()
    order_data["total_cost"] = total_cost
    order_data["delivery_status"] = "Pending"
    order_data["delivery_date"] = datetime.now()

    # Simulate saving the order (e.g., insert into DB)
    order_data["_id"] = str(order_data["order_id"])

    return order_data

# GET /order/{order_id} - Get an order by ID
@router.get("/{order_id}", response_description="Get an order by id", response_model=Order)
def get_order(order_id: str, request: Request):
    if (order := request.app.database["orders"].find_one({"order_id": order_id})) is not None:
        return order
    raise HTTPException(status_code=404, detail=f"Order with ID {order_id} not found")

# PUT /order/{order_id} - Update an order by ID
@router.put("/{order_id}", response_description="Update an order", response_model=Order)
def update_order(order_id: str, request: Request, order: OrderUpdate = Body(...)):
    update_data = {k: v for k, v in order.dict().items() if v is not None}
    if len(update_data) >= 1:
        update_result = request.app.database["orders"].update_one({"order_id": order_id}, {"$set": update_data})
        if update_result.modified_count == 0:
            raise HTTPException(status_code=404, detail=f"Order with ID {order_id} not found")

    if (existing_order := request.app.database["orders"].find_one({"order_id": order_id})) is not None:
        return existing_order

    raise HTTPException(status_code=404, detail=f"Order with ID {order_id} not found")

# DELETE /order/{order_id} - Delete an order by ID
@router.delete("/{order_id}", response_description="Delete an order")
def delete_order(order_id: str, request: Request):
    delete_result = request.app.database["orders"].delete_one({"order_id": order_id})

    if delete_result.deleted_count == 1:
        return {"message": "Order deleted successfully"}

    raise HTTPException(status_code=404, detail=f"Order with ID {order_id} not found")

# GET /order/search/user_id - Search orders by user_id
@router.get("/search/user_id", response_description="Search orders by user_id", response_model=List[Order])
def search_orders_by_user_id(user_id: str, request: Request):
    orders_cursor = list(request.app.database["orders"].find({"user_id": {"$regex": user_id, "$options": "i"}}))
    orders = []
    for order in orders_cursor:
        order["_id"] = str(order["_id"])  # Convert ObjectId to string
        orders.append(order)
    return orders


#http://127.0.0.1:8000/order/search/user_id?user_id=AG3D6O4STAQKAY2UVGEUV46KN35Q