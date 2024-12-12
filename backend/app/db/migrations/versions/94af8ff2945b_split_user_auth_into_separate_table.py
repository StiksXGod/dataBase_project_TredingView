"""Split user auth into separate table

Revision ID: 94af8ff2945b
Revises: 501fc472628d
Create Date: 2024-12-12 22:03:17.836899

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '94af8ff2945b'
down_revision: Union[str, None] = '501fc472628d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Создание таблицы user_auth
    op.create_table(
        'user_auth',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('refresh_token', sa.String(length=255), nullable=True),
        sa.Column('last_login', sa.TIMESTAMP(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('user_id')
    )

    # Перенос данных из users в user_auth
    op.execute("""
        INSERT INTO user_auth (user_id, password_hash, refresh_token)
        SELECT id, password_hash, refresh_token FROM users;
    """)

    # Удаление столбцов password и refresh_token из таблицы users
    op.drop_column('users', 'password_hash')
    op.drop_column('users', 'refresh_token')


def downgrade():
    # Добавление столбцов password и refresh_token обратно в таблицу users
    op.add_column('users', sa.Column('password_hash', sa.String(length=255), nullable=False))
    op.add_column('users', sa.Column('refresh_token', sa.String(length=255), nullable=True))

    # Перенос данных обратно из user_auth в users
    op.execute("""
        UPDATE users
        SET password = ua.password,
            refresh_token = ua.refresh_token
        FROM user_auth ua
        WHERE users.id = ua.user_id;
    """)

    # Удаление таблицы user_auth
    op.drop_table('user_auth')
