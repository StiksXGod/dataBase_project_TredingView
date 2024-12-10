"""Add refresh_token to Users

Revision ID: 44b6ba31e0bc
Revises: d0aa844851e8
Create Date: 2024-12-10 21:56:47.651652

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '44b6ba31e0bc'
down_revision: Union[str, None] = 'd0aa844851e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Добавляем новое поле refresh_token в таблицу Users
    op.execute("""
        ALTER TABLE Users
        ADD COLUMN refresh_token VARCHAR(255);
    """)


def downgrade() -> None:
    # Удаляем поле refresh_token из таблицы Users при откате миграции
    op.execute("""
        ALTER TABLE Users
        DROP COLUMN refresh_token;
    """)
