# pymongo-fastapi-crud/routes.py
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List, Optional
import httpx

from models import Product, ProductUpdate

router = APIRouter()

# POST /product - Create a new product
@router.post("/", response_description="Create a new product", status_code=status.HTTP_201_CREATED, response_model=Product)
async def create_product(request: Request, product: Product = Body(...)):
    async with httpx.AsyncClient() as client:
        # Query Product Service to get product details
        discount_url = f"http://127.0.0.1:8000/discount/{product.product_id}"
        discount_response = await client.get(discount_url)
        if discount_response.status_code != 200:
            raise HTTPException(status_code=discount_response.status_code, detail="Product not found")
        product_data = discount_response.json()

        actual_price = product_data.get("actual_price")
        discounted_price = product_data.get("discounted_price")
        discount_percentage = product_data.get("discount_percentage")
        if not actual_price or not discounted_price or not discount_percentage:
            raise HTTPException(status_code=404, detail="Product name not found")
        
        product_data = product.dict()
        product_data["actual_price"] = actual_price
        product_data["discounted_price"] = discounted_price
        product_data["discount_percentage"] = discount_percentage

        new_product = request.app.database["products"].insert_one(product_data)
        created_product = request.app.database["products"].find_one({"_id": new_product.inserted_id})

    return created_product  

# PUT /product/{id} - Update a product by ID
@router.put("/{id}", response_description="Update a product", response_model=Product)
def update_product(id: str, request: Request, product: ProductUpdate = Body(...)):
    product_data = {k: v for k, v in product.dict().items() if v is not None}
    if len(product_data) >= 1:
        update_result = request.app.database["products"].update_one({"_id": id}, {"$set": product_data})
        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with ID {id} not found")

    if (existing_product := request.app.database["products"].find_one({"_id": id})) is not None:
        return existing_product

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with ID {id} not found")


# DELETE /product/{id} - Delete a product by ID
@router.delete("/{id}", response_description="Delete a product")
def delete_product(id: str, request: Request, response: Response):
    delete_result = request.app.database["products"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with ID {id} not found")
#DELETE http://127.0.0.1:8000/product?id=67fd95fb9eda638327e5b6e5

# GET /product - List all products
@router.get("/", response_description="List all products", response_model=List[Product])
def list_products(request: Request):
    #return products
    products_cursor = request.app.database["products"].find(limit=100)
    
    # Convert the ObjectId to a string manually
    products = []
    for product in products_cursor:
        product["_id"] = str(product["_id"])
        products.append(product)
    
    return products

# GET /product/search/name - Search products by name
@router.get("/search/name", response_description="Search products by name", response_model=List[Product])
def search_by_name(name: str, request: Request):
    # Use a regular expression to search for products by name
    products_cursor = list(request.app.database["products"].find({"product_name": {"$regex": name, "$options": "i"}}))
    products = []
    for product in products_cursor:
        product["_id"] = str(product["_id"])
        products.append(product)
    return products

# GET /product/search/category - Search products by category
@router.get("/search/category", response_description="Search products by category", response_model=List[Product])
def search_by_category(category: str, request: Request):
    products_cursor = list(request.app.database["products"].find({"category": {"$regex": category, "$options": "i"}}))
    products = []
    for product in products_cursor:
        product["_id"] = str(product["_id"])
        products.append(product)
    return products

# GET /product/search/discount - Search products by product_id
@router.get("/{product_id}", response_description="Get a product by product_id", response_model=Product)
def get_product_by_product_id(product_id: str, request: Request):
    # Find the product by product_id in the database
    product = request.app.database["products"].find_one({"product_id": product_id})
    if product:
        product["_id"] = str(product["_id"])
        return product
    # If the product is not found, raise a 404 error
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with product_id {product_id} not found")

#http://127.0.0.1:8000/product/search/category?category=Electronics
#http://127.0.0.1:8000/product/search/name?name=Samsung

