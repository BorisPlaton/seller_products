from sqlalchemy import Column, Integer, String, Boolean, CheckConstraint, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression

from database.db import Base


class Product(Base):
    """
    Represents products that seller has.
    """
    __tablename__ = 'product'
    __table_args__ = (
        CheckConstraint("price > 0", name='product_price_is_natural_check'),
        CheckConstraint("quantity >= 0", name='product_quantity_is_positive_check'),
    )

    offer_id = Column(Integer, primary_key=True)
    name = Column(String(32))
    price = Column(Numeric)
    quantity = Column(Integer)
    available = Column(Boolean, server_default=expression.true())
    seller_id = Column(ForeignKey('seller.seller_id', ondelete='cascade'))

    seller = relationship('Seller', back_populates='products')


class Seller(Base):
    """
    Represents a seller with products which he has.
    """
    __tablename__ = 'seller'

    seller_id = Column(Integer, primary_key=True)

    products = relationship(Product, back_populates='seller')
