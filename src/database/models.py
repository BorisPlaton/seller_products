from sqlalchemy import Column, Integer, String, CheckConstraint, ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import relationship

from database.db import Base


class Product(Base):
    """
    Represents products that seller has.
    """
    __tablename__ = 'product'
    __table_args__ = (
        CheckConstraint("price > 0", name='product_price_is_natural_check'),
        CheckConstraint("offer_id > 0", name='offer_id_is_natural_check'),
        CheckConstraint("quantity >= 0", name='product_quantity_is_positive_check'),
        UniqueConstraint('offer_id', 'seller_id')
    )

    product_id = Column(Integer, primary_key=True)
    offer_id = Column(Integer, nullable=False)
    name = Column(String(32), nullable=False)
    price = Column(Numeric, nullable=False)
    quantity = Column(Integer, nullable=False)
    seller_id = Column(ForeignKey('seller.seller_id', ondelete='CASCADE'), nullable=False)

    seller = relationship('Seller', back_populates='products')

    def __repr__(self):
        return f"<Product: id-{self.product_id}, name-{self.name}>"


class Seller(Base):
    """
    Represents a seller with products which he has.
    """
    __tablename__ = 'seller'

    seller_id = Column(Integer, primary_key=True)

    products = relationship(Product, back_populates='seller')

    def __repr__(self):
        return f"<Seller: id-{self.seller_id}>"
