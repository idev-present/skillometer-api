"""fix event reply relation

Revision ID: 0fd8f6d06be3
Revises: d694c22fa28f
Create Date: 2024-06-16 17:07:45.480865

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0fd8f6d06be3'
down_revision: Union[str, None] = 'd694c22fa28f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('events_reply_id_fkey', 'events', type_='foreignkey')
    op.create_foreign_key(None, 'events', 'replies', ['reply_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'events', type_='foreignkey')
    op.create_foreign_key('events_reply_id_fkey', 'events', 'users', ['reply_id'], ['id'])
    # ### end Alembic commands ###
