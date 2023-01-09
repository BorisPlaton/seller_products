from typing import NamedTuple

from sqlalchemy import text
from sqlalchemy.orm import Session

from database.models import Seller
from products.schemas import ExcelProductRecord


class CreateUpdateStatistics(NamedTuple):
    """
    Represents statistics on the Insert on conflict Update
    query.
    """
    created: int
    updated: int


def create_new_seller() -> Seller:
    """
    Creates a new record for the `seller` table and returns it.
    """
    return Seller()


def create_product_on_conflict_update(
        session: Session, products: list[ExcelProductRecord], seller_id: int
) -> CreateUpdateStatistics:
    """
    Creates new product records. If some product already exists,
    then updates its field to the corresponding ones. Returns
    updated and created records quantity.
    """
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
    SELECT COALESCE(COUNT(*), 0) AS created_q
    FROM (SELECT offer_id FROM affected_rows
    EXCEPT
    SELECT offer_id FROM product) AS tmp;
    """), [{**dict(product), 'seller_id': seller_id} for product in products]).first()
    created_quantity = res.created_q
    return CreateUpdateStatistics(created=created_quantity, updated=len(products) - created_quantity)


def delete_products():
    pass
