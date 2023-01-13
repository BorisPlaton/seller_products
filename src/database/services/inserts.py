from sqlalchemy import text
from sqlalchemy.exc import ResourceClosedError
from sqlalchemy.orm import Session

from database.exceptions import DuplicateInsertError
from database.models import Seller
from database.services.structs import CreateUpdateStatistics, ProductRecord


def create_new_seller() -> Seller:
    """
    Creates a new record for the `seller` table and returns it.
    """
    return Seller()


def create_product_on_conflict_update(session: Session, products: list[ProductRecord]) -> CreateUpdateStatistics:
    """
    Creates new product records. If some product already exists,
    then updates its field to the corresponding ones. Returns
    updated and created records quantity.
    """
    if not products:
        raise ValueError("No products were provided for update/create operations.")
    try:
        res = session.execute(text("""
        WITH affected_rows AS (
            INSERT INTO product
                (offer_id, name, price, quantity, available, seller_id)
            VALUES
                (:offer_id, :name, :price, :quantity, :available, :seller_id)
            ON CONFLICT ON CONSTRAINT product_offer_id_seller_id_key
                DO UPDATE SET name = EXCLUDED.name,
                    price = EXCLUDED.price,
                    quantity = EXCLUDED.quantity,
                    available = EXCLUDED.available,
                    seller_id = EXCLUDED.seller_id
            RETURNING offer_id
        )
        SELECT COUNT(*) AS created_q
        FROM (SELECT offer_id FROM affected_rows
        EXCEPT
        SELECT offer_id FROM product) tmp;
        """), [product._asdict() for product in products]).first()
    except ResourceClosedError:
        raise DuplicateInsertError(
            "Create/update products failed. Check, if passed products don't have duplicates."
        )
    created_quantity = res.created_q
    return CreateUpdateStatistics(created=created_quantity, updated=len(products) - created_quantity)
