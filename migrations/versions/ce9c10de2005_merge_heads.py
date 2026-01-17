"""merge heads

Revision ID: ce9c10de2005
Revises: 514fbef3f3ca, a45e453eb5d6
Create Date: 2026-01-17 14:28:38.715254

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ce9c10de2005'
down_revision: Union[str, Sequence[str], None] = ('514fbef3f3ca', 'a45e453eb5d6')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
