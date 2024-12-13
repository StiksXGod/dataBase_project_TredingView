"""add image text

Revision ID: 06d4f759fdcb
Revises: 94af8ff2945b
Create Date: 2024-12-13 04:09:26.949880

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '06d4f759fdcb'
down_revision: Union[str, None] = '94af8ff2945b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('assets', sa.Column('descriptions', sa.Text(), nullable=True))


def downgrade():
    op.drop_column('assets', 'descriptions')
