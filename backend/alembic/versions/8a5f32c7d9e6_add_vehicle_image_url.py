"""add vehicle image_url column

Revision ID: 8a5f32c7d9e6
Revises: 2571f6984962
Create Date: 2026-07-12 17:30:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '8a5f32c7d9e6'
down_revision: Union[str, Sequence[str], None] = '2571f6984962'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'vehicles',
        sa.Column('image_url', sa.String(length=300), nullable=True),
    )


def downgrade() -> None:
    op.drop_column('vehicles', 'image_url')
