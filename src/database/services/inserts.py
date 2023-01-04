from database.models import Seller


def create_new_seller() -> Seller:
    """
    Creates a new record for the `seller` table and returns it.
    """
    return Seller()


def create_new_product():
    """
    Creates a new product for the specific seller.
    """
