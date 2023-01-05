from sqlalchemy.orm import Session
from starlette.requests import Request


def get_db_session(request: Request) -> Session:
    """
    Returns a SQLAlchemy Session object.
    """
    return request.state.session


def get_products_criteria(
        seller_id: int | None = None, offer_id: int | None = None,
        substring: str | None = None
) -> dict:
    """
    Returns only a specified products criteria dictionary.
    """
    products_criteria = {
        'seller_id': seller_id,
        'offer_id': offer_id,
        'substring': substring,
    }
    return {field: value for field, value in products_criteria.items() if value is not None}
