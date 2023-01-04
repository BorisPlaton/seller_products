from sqlalchemy.orm import Session

from database.models import Product


def get_filtered_products(session: Session, **kwargs) -> list[Product | None]:
    """
    Filters products by given key-word arguments and
    returns list of them.
    """
    results = session.query(Product).where(**kwargs).all()
    return results
