"""sync revision

Revision ID: 98b71a60bc84
Revises: ee9aa2d4507a
Create Date: 2024-04-28 00:54:09.372359

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '98b71a60bc84'
down_revision: Union[str, None] = 'ee9aa2d4507a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
