from sqlalchemy import text
from sqlalchemy.engine import Row
from sqlalchemy.orm import Session

from database.models import Seller
from database.services.structs import ProductRecord


def create_new_seller() -> Seller:
    """
    Creates a new record for the `seller` table and returns it.
    """
    return Seller()


def insert_product_on_conflict_update(session: Session, products: list[ProductRecord]) -> list[Row]:
    """
    Creates new product records. If some product already exists,
    then updates its field to the corresponding ones. Returns created
    products' ID.
    """
    if not products:
        raise ValueError("No products were provided for update/create operations.")
    res = session.execute(text("""
    INSERT INTO product
        (offer_id, name, price, quantity, seller_id)
    VALUES
        (:offer_id, :name, :price, :quantity, :seller_id)
    ON CONFLICT ON CONSTRAINT product_offer_id_seller_id_key
        DO UPDATE SET name = EXCLUDED.name,
            price = EXCLUDED.price,
            quantity = EXCLUDED.quantity,
            seller_id = EXCLUDED.seller_id
    RETURNING *;
    """), [product._asdict() for product in products]).all()
    return res
