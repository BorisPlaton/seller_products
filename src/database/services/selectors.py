from sqlalchemy.orm import Session, Query

from database.models import Product


def get_available_products(session: Session, **kwargs) -> Query:
    """
    Passes keyword arguments to the filter and returns
    Query instance. Returns only those instances, whose
    available column equals True.
    """
    kwargs.update({'available': True})
    return session.query(Product).filter_by(**kwargs)
