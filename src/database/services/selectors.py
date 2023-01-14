from sqlalchemy.orm import Session, Query

from database.models import Product


def get_all_products_by(session: Session, **kwargs) -> Query:
    """
    Passes keyword arguments to the filter and returns Query instance.
    """
    return session.query(Product).filter_by(**kwargs)


def get_filtered_products(session: Session, *args) -> Query:
    """
    Uses more complex `filter` statement instead of `filter_by`.
    """
    return session.query(Product).filter(*args)


def get_all_products_by_substring(session: Session, substring: str = None, **kwargs) -> list[Product]:
    """
    Returns all products. Keyword arguments are passed to the filter. The
    `substring` argument is used for LIKE operator with `%substring%` form.
    """
    filtered_products = get_all_products_by(session, **kwargs)
    if substring:
        filtered_products = filtered_products.filter(
            Product.name.like('%' + substring + '%')
        )
    return filtered_products.all()
