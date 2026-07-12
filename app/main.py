from fastapi import FastAPI
from app.routers import auth

from app.routers.products import router as products_router

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Welcome to Role Based E-commerce API"
    }

app.include_router(products_router)
app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"],
)