import pytest
from mixer.backend.sqlalchemy import mixer

from database.models import Seller
from database.services.inserts import create_product_on_conflict_update
from products.schemas import ExcelProductRecord


class TestProductInserts:

    @pytest.fixture
    def product(self):
        return ExcelProductRecord(**{
            'offer_id': 1,
            'name': "Book",
            'price': 450.5,
            'quantity': 13,
            'available': True
        })

    def test_create_product_on_conflict_update_creates_new_record(self, db_session, product):
        seller = mixer.blend(Seller)
        db_session.add(seller)
        db_session.flush()
        res = create_product_on_conflict_update(db_session, [product], seller.seller_id)
        assert not res.updated
        assert res.created == 1
