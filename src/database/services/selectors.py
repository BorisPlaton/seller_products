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


def get_all_products(
        session: Session, substring: str = None, **kwargs
) -> list[Product]:
    """
    Returns all products. Keyword arguments are passed to the filter. The
    `substring` argument is used for LIKE operator with `%substring%` form.
    """
    filtered_products = get_available_products(session, **kwargs)
    if substring:
        filtered_products = filtered_products.filter(
            Product.name.like('%' + substring + '%')
        )
    print(filtered_products)
    return filtered_products.all()
