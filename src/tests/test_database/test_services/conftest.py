import pytest
from mixer.backend.sqlalchemy import mixer

from database.models import Seller
from database.services.structs import ProductRecord, DeleteProductData


@pytest.fixture
def seller(db_session) -> Seller:
    seller = mixer.blend(Seller)
    db_session.add(seller)
    db_session.flush()
    return seller


@pytest.fixture
def product(seller):
    return ProductRecord(**{
        'offer_id': 1,
        'name': "Book",
        'price': 450.5,
        'quantity': 13,
        'available': True,
        'seller_id': seller.seller_id
    })


@pytest.fixture
def product_for_delete(product) -> DeleteProductData:
    return DeleteProductData(
        seller_id=product.seller_id, offer_id=product.offer_id
    )
