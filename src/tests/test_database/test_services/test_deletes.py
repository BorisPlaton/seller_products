from sqlalchemy import select

from database.models import Product
from database.services.deletes import delete_products_by_records


class TestDeletes:

    def test_delete_product_with_wrong_id_returns_zero_quantity(self, db_session, product_for_delete):
        quantity = delete_products_by_records(db_session, [product_for_delete])
        assert not quantity

    def test_delete_product_return_exact_number_of_deleted_rows(
            self, db_session, product, product_for_delete, conn
    ):
        db_session.add(Product(**product._asdict()))
        assert db_session.query(Product).count() == 1
        quantity = delete_products_by_records(db_session, [product_for_delete])
        assert quantity == 1
        assert not conn.execute(select(Product)).all()
