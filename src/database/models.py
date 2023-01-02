from sqlalchemy import Column, Integer, String, Boolean, CheckConstraint, ForeignKey
from sqlalchemy.orm import validates, relationship
from sqlalchemy.sql import expression

from database.db import Base


class Offer(Base):
    """
    The seller's offer with products relationship.
    """
    __tablename__ = 'offer'
    offer_id = Column(Integer, primary_key=True)
    seller_id = Column(ForeignKey('seller.seller_id', ondelete='cascade'))
    product_id = Column(ForeignKey('product.product_id', ondelete='cascade'))

    seller = relationship('Seller', back_populates='offers')
    products = relationship('Product', back_populates='offers')


class Product(Base):
    """
    Represents products that are in the offer.
    """
    __tablename__ = 'product'
    __table_args__ = (
        CheckConstraint("price > 0", name='product_price_is_natural_check'),
        CheckConstraint("quantity >= 0", name='product_quantity_is_positive_check'),
    )

    product_id = Column(Integer, primary_key=True)
    name = Column(String(32))
    price = Column(Integer)
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

    products = relationship('Seller', back_populates='seller')
