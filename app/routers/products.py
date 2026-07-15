from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import status
from app.dependencies.database import get_db
from app.schemas.product import ProductCreate, ProductResponse
from app.services.product_service import ProductService
from app.dependencies.roles import require_seller
from app.models.user import User

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.post("/", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_seller),
):
    return ProductService.create_product(
        db,
        product,
        current_user,
    )

@router.get("/", response_model=list[ProductResponse])
def get_products(
    db: Session = Depends(get_db)
):
    return ProductService.get_all_products(db)

@router.get("/{product_id}", response_model=ProductResponse)
def get_product_by_id(
    product_id: int,
    db: Session = Depends(get_db),
):
    return ProductService.get_product_by_id(db, product_id)

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_seller),
):
    return ProductService.update_product(
        db,
        product_id,
        product,
        current_user,
    )

@router.delete(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_seller),
):
    return ProductService.delete_product(
        db,
        product_id,
        current_user,
    )