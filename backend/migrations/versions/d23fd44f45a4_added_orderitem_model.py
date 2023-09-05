"""
added OrderItem model 

Revision ID: d23fd44f45a4
Revises: 92edc6488914
Create Date: 2023-09-05 10:40:28.100476

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from src.app.enums import OrderItemStatusEnum  # Import your OrderItemStatusEnum

# revision identifiers, used by Alembic.
revision: str = 'd23fd44f45a4'
down_revision: Union[str, None] = '92edc6488914'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'order_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uuid', UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), unique=True, nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('total_price', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=30), server_default=str(OrderItemStatusEnum.PENDING_PAYMENT), nullable=False),
        sa.Column('order_id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('vendor_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
        sa.ForeignKeyConstraint(['vendor_id'], ['vendors.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
    # You might need to add an index or other constraints based on your requirements


def downgrade() -> None:
    op.drop_table('order_items')

