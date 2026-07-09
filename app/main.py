from fastapi import FastAPI

from app.routers.products import router as products_router

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Welcome to Role Based E-commerce API"
    }

app.include_router(products_router)