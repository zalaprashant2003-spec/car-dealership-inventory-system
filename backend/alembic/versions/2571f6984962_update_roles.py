"""update roles

Revision ID: 2571f6984962
Revises: 14712ab6e2e4
Create Date: 2026-07-12 11:10:44.652809

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2571f6984962'
down_revision: Union[str, Sequence[str], None] = '14712ab6e2e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Convert existing managers to customer to prevent cast error
    op.execute("UPDATE users SET role = 'SALESPERSON' WHERE role = 'MANAGER'")
    
    # Create new enum and swap
    op.execute("ALTER TYPE userrole RENAME TO userrole_old")
    op.execute("CREATE TYPE userrole AS ENUM('ADMIN', 'SALESPERSON', 'CUSTOMER')")
    op.execute("ALTER TABLE users ALTER COLUMN role DROP DEFAULT")
    op.execute("ALTER TABLE users ALTER COLUMN role TYPE userrole USING role::text::userrole")
    op.execute("ALTER TABLE users ALTER COLUMN role SET DEFAULT 'CUSTOMER'")
    op.execute("DROP TYPE userrole_old")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("ALTER TYPE userrole RENAME TO userrole_new")
    op.execute("CREATE TYPE userrole AS ENUM('ADMIN', 'MANAGER', 'SALESPERSON')")
    op.execute("ALTER TABLE users ALTER COLUMN role DROP DEFAULT")
    op.execute("ALTER TABLE users ALTER COLUMN role TYPE userrole USING role::text::userrole")
    op.execute("ALTER TABLE users ALTER COLUMN role SET DEFAULT 'SALESPERSON'")
    op.execute("DROP TYPE userrole_new")
