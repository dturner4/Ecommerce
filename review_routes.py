from fastapi import status, APIRouter, HTTPException, Request, Body, status, Response
from typing import List
from models import Review, ReviewUpdate
from pymongo import MongoClient
import httpx

router = APIRouter()

# GET /review/search/username - Search reviews by username
@router.get("/search/username", response_description="Search reviews by username", response_model=List[Review])
def search_reviews_by_username(username: str, request: Request):
    reviews_cursor = list(request.app.database["reviews"].find({"user_name": {"$regex": username, "$options": "i"}}))
    reviews = []
    
    for review in reviews_cursor:
        review["_id"] = str(review["_id"]) 
        reviews.append(review)
    
    return reviews
#http://127.0.0.1:8000/review/search/username?username=Manav


# POST /review - Create a new review
@router.post("/", response_description="Create a new product", status_code=status.HTTP_201_CREATED, response_model=Review)
async def create_product(request: Request, review: Review = Body(...)):
    async with httpx.AsyncClient() as client:
        review_url = f"http://127.0.0.1:8000/product/{review.product_id}"
        review_response = await client.get(review_url)
        if review_response.status_code != 200:
            raise HTTPException(status_code=review_response.status_code, detail="Product not found")
        product_data = review_response.json()

        product_link = product_data.get("product_link")
        img_link = product_data.get("img_link")
        if not product_link or not img_link:
            raise HTTPException(status_code=404, detail="Product name not found")
        
        reveiw_data = review.dict()
        reveiw_data["product_link"] = product_link
        reveiw_data["img_link"] = img_link

    return reveiw_data

# PUT /review/{review_id} - Update a review by ID
@router.put("/{review_id}", response_description="Update a review", response_model=Review)
def update_review(review_id: str, request: Request, review: ReviewUpdate):
    update_data = {k: v for k, v in review.dict().items() if v is not None}
    if len(update_data) >= 1:
        update_result = request.app.database["reviews"].update_one({"review_id": review_id}, {"$set": update_data})
        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Review with ID {review_id} not found")
    
    if (existing_review := request.app.database["reviews"].find_one({"review_id": review_id})) is not None:
        return existing_review

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Review with ID {review_id} not found")

# DELETE /review/{review_id} - Delete a review by ID
@router.delete("/{review_id}", response_description="Delete a review")
def delete_review(review_id: str, request: Request, response: Response):
    delete_result = request.app.database["reviews"].delete_one({"review_id": review_id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Review with ID {review_id} not found")
