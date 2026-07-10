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
        return db.query(Product).all()