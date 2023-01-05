from sqlalchemy.orm import Session

from database.models import Product
from database.services.selectors import get_available_products


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
