"""add document processing fields

Revision ID: bcffcf306ac7
Revises: e540e730e3be
Create Date: 2026-01-19 18:50:20.178997

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bcffcf306ac7'
down_revision: Union[str, Sequence[str], None] = 'e540e730e3be'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
