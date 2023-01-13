from sqlalchemy import tuple_
from sqlalchemy.orm import Session

from database.models import Product
from database.services.structs import DeleteProductData


def delete_products_by_records(session: Session, product_records: list[DeleteProductData]) -> int:
    """
    Deletes specific products by their seller and offer id. Returns the quantity
    of deleted products.
    """
    return session.query(Product).where(
        tuple_(Product.seller_id, Product.offer_id).in_(
            [(product.seller_id, product.offer_id) for product in product_records]
        )
    ).delete()
