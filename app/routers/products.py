from fastapi import APIRouter
from app.schemas.product import ProductCreate

router = APIRouter()

products = []


@router.get("/products")
def get_products():
    return products


@router.post("/products")
def create_product(product: ProductCreate):
    products.append(product)

    return {
        "message": "Product added successfully"
    }