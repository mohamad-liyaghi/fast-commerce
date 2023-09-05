"""
added Order model 

Revision ID: 92edc6488914
Revises: a4cc793d6444
Create Date: 2023-09-05 10:33:21.467971

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from src.app.enums import OrderStatusEnum  # Import your OrderStatusEnum

# revision identifiers, used by Alembic.
revision: str = '92edc6488914'
down_revision: Union[str, None] = 'a4cc793d6444'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'orders',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uuid', UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), unique=True, nullable=False),
        sa.Column('delivery_address', sa.String(length=120), nullable=False),
        sa.Column('total_price', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('status', sa.String(length=30), server_default=str(OrderStatusEnum.PENDING_PAYMENT), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
    # You might need to add an index or other constraints based on your requirements


def downgrade() -> None:
    op.drop_table('orders')

