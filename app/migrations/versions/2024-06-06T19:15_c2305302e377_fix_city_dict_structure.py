"""fix city dict structure

Revision ID: c2305302e377
Revises: 919d2df7f11c
Create Date: 2024-06-06 19:15:37.926084

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2305302e377'
down_revision: Union[str, None] = '919d2df7f11c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dict_city', sa.Column('name', sa.String(length=50), nullable=True))
    op.alter_column('vacancies', 'city_id',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('vacancies', 'city_id',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    op.drop_column('dict_city', 'name')
    # ### end Alembic commands ###
