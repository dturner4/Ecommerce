from fastapi import APIRouter, Request, HTTPException, Body, status
from typing import List
from models import Discount, DiscountUpdate

router = APIRouter()

# POST /discount - Create a new discount
@router.post("/", response_description="Create a new discount", status_code=201, response_model=Discount)
def create_discount(request: Request, discount: Discount = Body(...)):
    discount_data = discount.dict()
    new_discount = request.app.database["discounts"].insert_one(discount_data)
    created_discount = request.app.database["discounts"].find_one({"_id": new_discount.inserted_id})
    return created_discount



# PUT /discount/{id} - Update a discount by ID
@router.put("/{product_id}", response_description="Update a discount", response_model=Discount)
def update_discount(product_id: str, request: Request, discount: DiscountUpdate = Body(...)):
    update_data = {k: v for k, v in discount.dict().items() if v is not None}
    if len(update_data) >= 1:
        update_result = request.app.database["discounts"].update_one({"product_id": product_id}, {"$set": update_data})
        if update_result.modified_count == 0:
            raise HTTPException(status_code=404, detail=f"Discount with ID {id} not found")

    if (existing_discount := request.app.database["discounts"].find_one({"product_id": product_id})) is not None:
        return existing_discount

    raise HTTPException(status_code=404, detail=f"Discount with ID {id} not found")

# DELETE /discount/{id} - Delete a discount by ID
@router.delete("/{product_id}", response_description="Delete a discount")
def delete_discount(product_id: str, request: Request):
    delete_result = request.app.database["discounts"].delete_one({"product_id": product_id})

    if delete_result.deleted_count == 1:
        return {"message": "Discount deleted successfully"}

    raise HTTPException(status_code=404, detail=f"Discount with ID {id} not found")

# GET /discount/search/product_id - Search discounts by product_id
@router.get("/search/product_id", response_description="Search discounts by product_id", response_model=List[Discount])
def search_discount_by_product_id(product_id: str, request: Request):
    discounts_cursor = list(request.app.database["discounts"].find({"product_id": {"$regex": product_id, "$options": "i"}}))
    discounts = []
    for discount in discounts_cursor:
        discount["_id"] = str(discount["_id"])
        discounts.append(discount)
    return discounts

# GET /discount/{product_id} - Get a discount by product_id, used by other services
@router.get("/{product_id}", response_description="Get a product by product_id", response_model=Discount)
def get_product_by_product_id(product_id: str, request: Request):
    product = request.app.database["discounts"].find_one({"product_id": product_id})
    if product:
        product["_id"] = str(product["_id"])
        return product
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with product_id {product_id} not found")
