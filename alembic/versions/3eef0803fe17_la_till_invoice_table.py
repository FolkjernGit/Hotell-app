"""la till invoice table

Revision ID: 3eef0803fe17
Revises: 7e2dcb82a099
Create Date: 2025-11-27 10:43:40.883890

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '3eef0803fe17'
down_revision: Union[str, Sequence[str], None] = '7e2dcb82a099'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # 1. Add missing room_id column
    op.add_column(
        'bookings',
        sa.Column('room_id', sa.Integer(), nullable=True)
    )

    # 2. Add foreign key to rooms.id
    op.create_foreign_key(
        op.f('fk_bookings_room_id_rooms'),
        'bookings',
        'rooms',
        ['room_id'],
        ['id']
    )


def downgrade() -> None:
    """Downgrade schema."""

    # Drop FK first
    op.drop_constraint(
        op.f('fk_bookings_room_id_rooms'),
        'bookings',
        type_='foreignkey'
    )

    # Drop the added column
    op.drop_column('bookings', 'room_id')
