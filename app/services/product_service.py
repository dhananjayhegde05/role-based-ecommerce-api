from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate
from app.models.user import User, UserRole


class ProductService:

    @staticmethod
    def create_product(
            db: Session,
            product: ProductCreate,
            current_user: User,
    ) -> Product:
        new_product = Product(
            name=product.name,
            price=product.price,
            stock=product.stock,
            owner_id=current_user.id,
        )

        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        return new_product

    @staticmethod
    def get_all_products(db: Session):
        stmt = select(Product)

        result = db.execute(stmt)

        return result.scalars().all()

    @staticmethod
    def get_product_by_id(db: Session, product_id: int):
        stmt = select(Product).where(Product.id == product_id)

        result = db.execute(stmt)

        product = result.scalar_one_or_none()

        if product is None:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        return product

    @staticmethod
    def update_product(
            db: Session,
            product_id: int,
            product_data: ProductCreate,
            current_user: User,
    ):
        product = ProductService.get_product_by_id(db, product_id)

        if (
                current_user.role != UserRole.ADMIN
                and product.owner_id != current_user.id
        ):
            raise HTTPException(
                status_code=403,
                detail="Not authorized to update this product",
            )

        product.name = product_data.name
        product.price = product_data.price
        product.stock = product_data.stock

        db.commit()
        db.refresh(product)

        return product

    @staticmethod
    def delete_product(
            db: Session,
            product_id: int,
            current_user: User,
    ):
        product = ProductService.get_product_by_id(db, product_id)

        if (
                current_user.role != UserRole.ADMIN
                and product.owner_id != current_user.id
        ):
            raise HTTPException(
                status_code=403,
                detail="Not authorized to delete this product",
            )

        db.delete(product)
        db.commit()

        return {
            "message": "Product deleted successfully"
        }