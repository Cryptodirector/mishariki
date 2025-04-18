"""first

Revision ID: 7125799be96b
Revises: 
Create Date: 2025-04-17 12:43:58.687752

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7125799be96b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('popular_products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('descriptions', sa.String(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('old_price', sa.Integer(), nullable=True),
    sa.Column('url_photo', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_photo_cover',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('guest', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('descriptions', sa.String(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('old_price', sa.Integer(), nullable=True),
    sa.Column('url_photo', sa.String(), nullable=True),
    sa.Column('categories_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['categories_id'], ['categories.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('products_users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_products', sa.Integer(), nullable=False),
    sa.Column('id_users', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_products'], ['products.id'], ),
    sa.ForeignKeyConstraint(['id_users'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('products_users')
    op.drop_table('products')
    op.drop_table('users')
    op.drop_table('user_photo_cover')
    op.drop_table('popular_products')
    op.drop_table('categories')
    # ### end Alembic commands ###
