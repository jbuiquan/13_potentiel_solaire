"""move DROMS geometries to their real position and size

Revision ID: ead6345a90bc
Revises: 9cdde941f829
Create Date: 2025-03-30 21:55:15.454331

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ead6345a90bc'
down_revision: Union[str, None] = '9cdde941f829'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
