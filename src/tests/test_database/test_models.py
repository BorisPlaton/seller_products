import pytest
from mixer.backend.sqlalchemy import mixer
from sqlalchemy.exc import IntegrityError

from database.models import Seller, Product


class TestSellerModel:

    def test_model_can_be_created(self, db_session):
        model = Seller()
        db_session.add(model)
        db_session.flush()
        assert model.seller_id


class TestProductModel:

    @pytest.mark.parametrize(
        'offer_id', [0, -1]
    )
    def test_offer_id_must_be_greater_than_zero(self, db_session, offer_id):
        product = mixer.blend(Product, offer_id=offer_id, price=1, quantity=1)
        with pytest.raises(IntegrityError):
            db_session.add(product)
            db_session.commit()

    @pytest.mark.parametrize(
        'price', [0, -1]
    )
    def test_price_must_be_greater_than_zero(self, db_session, price, get_product):
        product = get_product(offer_id=1, price=price, quantity=1)
        with pytest.raises(IntegrityError):
            db_session.add(product)
            db_session.commit()

    def test_quantity_must_be_greater_or_equal_than_zero(self, db_session, get_product):
        seller = mixer.blend(Seller)
        with pytest.raises(IntegrityError), db_session.begin(nested=True):
            db_session.add(get_product(offer_id=1, price=1, quantity=-1, seller=seller))
            db_session.commit()
        seller = mixer.blend(Seller)
        product = get_product(offer_id=1, price=1, quantity=0, seller=seller)
        db_session.add(product)
        db_session.flush()
        assert product.product_id
        assert not product.quantity
        assert product.seller.seller_id == seller.seller_id

    def test_offer_id_and_seller_id_must_be_unique_together(self, db_session, get_product):
        seller = mixer.blend(Seller)
        db_session.add(seller)
        db_session.flush()
        product1 = get_product(offer_id=1, seller=seller, price=1, quantity=1)
        product2 = get_product(offer_id=1, seller=seller, price=1, quantity=1)
        with pytest.raises(IntegrityError):
            db_session.add_all([product1, product2])
            db_session.commit()

    def test_product_and_seller_are_dynamically_updated(self, db_session, get_product):
        seller = mixer.blend(Seller)
        product = get_product(offer_id=1, seller=seller, price=1, quantity=1)
        db_session.add(product)
        db_session.flush()
        assert product in seller.products
