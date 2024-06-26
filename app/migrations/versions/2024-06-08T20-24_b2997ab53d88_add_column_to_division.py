"""add column to division

Revision ID: b2997ab53d88
Revises: c12d45f876a7
Create Date: 2024-06-08 20:24:45.767778

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2997ab53d88'
down_revision: Union[str, None] = 'c12d45f876a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dict_division', sa.Column('group', sa.String(length=50), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    pass
