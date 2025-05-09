# models.py
import uuid
from pydantic import BaseModel, Field
from bson import ObjectId 
from typing import Optional
from datetime import datetime

def str_id(obj: ObjectId) -> str:
    return str(obj)

class Product(BaseModel):
    product_id: str
    product_name: str
    category: str
    discounted_price: str = None
    actual_price: str = None
    discount_percentage: str = None
    rating: str
    rating_count: str
    about_product: str
    img_link: str
    product_link: str

    # Ensure the _id field is converted to string when returning the response
    class Config:
        json_encoders = {
            ObjectId: str_id
        }


class ProductUpdate(BaseModel):
    product_name: Optional[str]
    category: Optional[str]
    discounted_price: Optional[str]
    actual_price: Optional[str]
    discount_percentage: Optional[str]
    rating: Optional[str]
    rating_count: Optional[str]
    about_product: Optional[str]
    img_link: Optional[str]
    product_link: Optional[str]

class Review(BaseModel):
    review_id: str
    user_id: str
    user_name: str
    review_title: str
    review_content: str
    product_link: str = None
    img_link: str = None
    product_id: str

class ReviewUpdate(BaseModel):
    review_title: Optional[str] = None
    review_content: Optional[str] = None
    product_link: Optional[str] = None
    img_link: Optional[str] = None
    product_id: Optional[str] = None


class Discount(BaseModel):
    product_id: str
    product_name: str
    actual_price: str
    discount_percentage: str
    discounted_price: str

class DiscountUpdate(BaseModel):
    product_name: Optional[str] = None
    actual_price: Optional[str] = None
    discount_percentage: Optional[str] = None
    discounted_price: Optional[str] = None



class Order(BaseModel):
    user_id: str
    order_id: str
    product_id: str
    product_ordered: str = None
    quantity: int
    total_cost: float = None
    delivery_status: str = "Pending"
    delivery_date: datetime = None
    class Config:
        json_encoders = {
            ObjectId: str  # Convert ObjectId to string when returning it in the response
        }
class OrderUpdate(BaseModel):
    product_ordered: Optional[str] = None
    quantity: Optional[int] = None
    total_cost: Optional[float] = None
    delivery_status: Optional[str] = None
    delivery_date: Optional[datetime] = None