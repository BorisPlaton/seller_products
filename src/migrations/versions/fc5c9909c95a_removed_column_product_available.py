"""Removed column 'product.available'

Revision ID: fc5c9909c95a
Revises: c65b3f4afea1
Create Date: 2023-01-14 19:01:26.418139

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc5c9909c95a'
down_revision = 'c65b3f4afea1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product', 'available')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('available', sa.BOOLEAN(), server_default=sa.text('true'), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
