import pytest
from sqlalchemy.engine import Row

from database.services.inserts import insert_product_on_conflict_update


class TestProductInserts:

    def test_create_product_on_conflict_update_creates_new_record(self, db_session, product):
        res = insert_product_on_conflict_update(db_session, [product])
        assert isinstance(res, list)
        assert isinstance(res[0], Row)
        assert len(res) == 1

    def test_create_and_update_with_empty_list_returns_zero(self, db_session):
        with pytest.raises(ValueError):
            insert_product_on_conflict_update(db_session, [])
