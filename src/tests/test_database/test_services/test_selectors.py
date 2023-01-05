from database.models import Product
from database.services.selectors import get_available_products


class TestProductSelectors:

    def test_get_available_products_without_kwargs_returns_all_products(self, db_session, get_product):
        product = get_product()
        db_session.add(product)
        assert db_session.query(Product).count() == 1
        products = get_available_products(db_session).all()
        assert isinstance(products, list)
        assert products[0] == product

    def test_get_available_products_returns_empty_list_if_none_matches_filter(self, db_session, get_product):
        product = get_product()
        db_session.add(product)
        products = get_available_products(db_session, product_id=0).all()
        assert isinstance(products, list)
        assert not products

    def test_get_available_products_returns_only_available_products(self, db_session, get_product):
        deleted_product = get_product(available=False)
        db_session.add(deleted_product)
        assert db_session.query(Product).count() == 1
        products = get_available_products(db_session).all()
        assert not products
