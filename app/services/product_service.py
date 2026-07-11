from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate


class ProductService:

    @staticmethod
    def create_product(db: Session, product: ProductCreate) -> Product:
        new_product = Product(
            name=product.name,
            price=product.price,
            stock=product.stock,
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
    ):
        # Step 1: Get existing product (raises 404 if not found)
        product = ProductService.get_product_by_id(db, product_id)

        # Step 2: Update the object's attributes
        product.name = product_data.name
        product.price = product_data.price
        product.stock = product_data.stock

        # Step 3: Save changes to the database
        db.commit()

        # Step 4: Reload the updated object
        db.refresh(product)

        # Step 5: Return updated product
        return product

    @staticmethod
    def delete_product(
            db: Session,
            product_id: int,
    ):
        # Step 1: Get the product (raises 404 if not found)
        product = ProductService.get_product_by_id(db, product_id)

        # Step 2: Delete the product
        db.delete(product)

        # Step 3: Commit the transaction
        db.commit()

        return {
            "message": "Product deleted successfully"
        }