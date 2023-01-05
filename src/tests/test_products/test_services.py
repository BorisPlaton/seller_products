from products.services.selectors import get_all_products


class TestProductServices:

    def test_get_all_products_without_kwargs_and_substring_returns_all_products(self, db_session, get_product):
        products_quantity = 10
        generated_products = [get_product() for _ in range(products_quantity)]
        db_session.add_all(generated_products)
        products = get_all_products(db_session)
        assert len(products) == products_quantity
        for product in generated_products:
            assert product in products

    def test_get_all_products_with_substring_returns_all_product_matched_it(self, db_session, get_product):
        first_product = get_product(name='apple')
        second_product = get_product(name='pineapple')
        db_session.add_all([first_product, second_product])
        products = get_all_products(db_session, 'apple')
        assert len(products) == 2
        assert first_product in products
        assert second_product in products
