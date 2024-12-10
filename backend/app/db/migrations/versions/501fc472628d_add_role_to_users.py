"""Add role to Users

Revision ID: 501fc472628d
Revises: 44b6ba31e0bc
Create Date: 2024-12-11 00:52:11.877566

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '501fc472628d'
down_revision: Union[str, None] = '44b6ba31e0bc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('users', sa.Column('role', sa.String(length=50), nullable=False, server_default='user'))

def downgrade():
    op.drop_column('users', 'role')
