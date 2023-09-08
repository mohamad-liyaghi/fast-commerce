"""fix_enums

Revision ID: bfa69f41906e
Revises: 62d8af1cf62f
Create Date: 2023-09-08 09:45:42.185720

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'bfa69f41906e'
down_revision: Union[str, None] = '62d8af1cf62f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass

def downgrade() -> None:
    pass
