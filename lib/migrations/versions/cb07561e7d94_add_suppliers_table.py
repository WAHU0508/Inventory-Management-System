"""Add suppliers table

Revision ID: cb07561e7d94
Revises: 5f2967cd2d80
Create Date: 2024-09-17 18:26:46.965920

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cb07561e7d94'
down_revision: Union[str, None] = '5f2967cd2d80'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('suppliers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('contact', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column('categories', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('items', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('items', 'price',
               existing_type=sa.DECIMAL(precision=10, scale=2),
               nullable=False)
    op.alter_column('stocklevels', 'quantity',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('stocklevels', 'quantity',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('items', 'price',
               existing_type=sa.DECIMAL(precision=10, scale=2),
               nullable=True)
    op.alter_column('items', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('categories', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_table('suppliers')
    # ### end Alembic commands ###
