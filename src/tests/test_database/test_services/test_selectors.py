from database.models import Product
from database.services.selectors import get_all_products_by, get_all_products_by_substring


class TestProductSelectors:

    def test_get_available_products_without_kwargs_returns_all_products(self, db_session, get_product):
        product = get_product()
        db_session.add(product)
        assert db_session.query(Product).count() == 1
        products = get_all_products_by(db_session).all()
        assert isinstance(products, list)
        assert products[0] == product

    def test_get_available_products_returns_empty_list_if_none_matches_filter(self, db_session, get_product):
        product = get_product()
        db_session.add(product)
        products = get_all_products_by(db_session, product_id=0).all()
        assert isinstance(products, list)
        assert not products

    def test_get_all_products_without_kwargs_and_substring_returns_all_products(self, db_session, get_product):
        products_quantity = 10
        generated_products = [get_product() for _ in range(products_quantity)]
        db_session.add_all(generated_products)
        products = get_all_products_by_substring(db_session)
        assert len(products) == products_quantity
        for product in generated_products:
            assert product in products

    def test_get_all_products_with_substring_returns_all_product_matched_it(self, db_session, get_product):
        first_product = get_product(name='apple')
        second_product = get_product(name='pineapple')
        db_session.add_all([first_product, second_product])
        products = get_all_products_by_substring(db_session, 'apple')
        assert len(products) == 2
        assert first_product in products
        assert second_product in products
