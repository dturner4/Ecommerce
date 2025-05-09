# pymongo-fastapi-crud/main.py
from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from product_routes import router as product_router
from review_routes import router as review_router
from discount_routes import router as discount_router
from order_routes import router as order_router

config = dotenv_values(".env")

app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "Welcome to the Product API"}

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(product_router, tags=["products"], prefix="/product")
app.include_router(discount_router, prefix="/discount", tags=["discount"])
app.include_router(order_router, prefix="/order", tags=["order"])
app.include_router(review_router, prefix="/review", tags=["review"])

"""cd C:\Users\turnerd\OneDrive - Milwaukee School of Engineering\Desktop\Senior Year\microserviceproject
env-pymongo-fastapi-crud\Scripts\activate
python -m uvicorn main:app --reload"""