import pytest

from database.services.inserts import create_product_on_conflict_update


class TestProductInserts:

    def test_create_product_on_conflict_update_creates_new_record(self, db_session, product):
        res = create_product_on_conflict_update(db_session, [product])
        assert not res.updated
        assert res.created == 1

    def test_create_and_update_with_empty_list_returns_zero(self, db_session):
        with pytest.raises(ValueError):
            create_product_on_conflict_update(db_session, [])
