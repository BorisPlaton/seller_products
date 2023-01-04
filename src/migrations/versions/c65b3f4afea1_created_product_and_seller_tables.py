"""Created Product and Seller tables

Revision ID: c65b3f4afea1
Revises:
Create Date: 2023-01-04 17:37:37.010555

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c65b3f4afea1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'seller',
        sa.Column('seller_id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('seller_id')
    )
    op.create_table(
        'product',
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('offer_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=32), nullable=False),
        sa.Column('price', sa.Numeric(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('available', sa.Boolean(), server_default=sa.text('true'), nullable=False),
        sa.Column('seller_id', sa.Integer(), nullable=False),
        sa.CheckConstraint('offer_id > 0', name='offer_id_is_natural_check'),
        sa.CheckConstraint('price > 0', name='product_price_is_natural_check'),
        sa.CheckConstraint('quantity >= 0', name='product_quantity_is_positive_check'),
        sa.ForeignKeyConstraint(['seller_id'], ['seller.seller_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('product_id'),
        sa.UniqueConstraint('offer_id', 'seller_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('product')
    op.drop_table('seller')
    # ### end Alembic commands ###
