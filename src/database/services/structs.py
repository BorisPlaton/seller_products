from typing import NamedTuple


class CreateUpdateStatistics(NamedTuple):
    """
    Represents statistics on the Insert on conflict Update
    query.
    """
    created: int
    updated: int


class ProductRecord(NamedTuple):
    """
    Represents a product record from the database.
    """
    offer_id: int
    seller_id: int
    name: str
    price: float
    quantity: int
    available: bool


class DeleteProductData(NamedTuple):
    """
    Represents data that is necessarily for delete operations.
    """
    seller_id: int
    offer_id: int
