from sqlalchemy import Column, Integer, String, Boolean, CheckConstraint
from sqlalchemy.orm import validates
from sqlalchemy.sql import expression

from database.db import Base


class Product(Base):
    """
    Represents products that are received from the seller.
    """
    __tablename__ = 'products'
    __table_args__ = (
        CheckConstraint("price > 0", name='product_price_is_natural_check'),
        CheckConstraint("quantity >= 0", name='product_quantity_is_positive_check'),
    )

    offer_id = Column(Integer, primary_key=True)
    name = Column(String(32))
    price = Column(Integer)
    quantity = Column(Integer)
    available = Column(Boolean, server_default=expression.true())
