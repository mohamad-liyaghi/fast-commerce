"""updated uuid field

Revision ID: faeb555b207a
Revises: d23fd44f45a4
Create Date: 2023-09-05 12:50:00.780665

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'faeb555b207a'
down_revision: Union[str, None] = 'd23fd44f45a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('order_items', 'uuid',
               existing_type=sa.UUID(),
               nullable=True,
               existing_server_default=sa.text('gen_random_uuid()'))
    op.alter_column('order_items', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True,
               existing_server_default=sa.text('now()'))
    op.alter_column('order_items', 'status',
               existing_type=sa.VARCHAR(length=30),
               nullable=True,
               existing_server_default=sa.text("'OrderItemStatusEnum.PENDING_PAYMENT'::character varying"))
    op.create_index(op.f('ix_order_items_id'), 'order_items', ['id'], unique=False)
    op.alter_column('orders', 'uuid',
               existing_type=sa.UUID(),
               nullable=True,
               existing_server_default=sa.text('gen_random_uuid()'))
    op.alter_column('orders', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True,
               existing_server_default=sa.text('now()'))
    op.alter_column('orders', 'status',
               existing_type=sa.VARCHAR(length=30),
               nullable=True,
               existing_server_default=sa.text("'OrderStatusEnum.PENDING_PAYMENT'::character varying"))
    op.create_index(op.f('ix_orders_id'), 'orders', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_orders_id'), table_name='orders')
    op.alter_column('orders', 'status',
               existing_type=sa.VARCHAR(length=30),
               nullable=False,
               existing_server_default=sa.text("'OrderStatusEnum.PENDING_PAYMENT'::character varying"))
    op.alter_column('orders', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False,
               existing_server_default=sa.text('now()'))
    op.alter_column('orders', 'uuid',
               existing_type=sa.UUID(),
               nullable=False,
               existing_server_default=sa.text('gen_random_uuid()'))
    op.drop_index(op.f('ix_order_items_id'), table_name='order_items')
    op.alter_column('order_items', 'status',
               existing_type=sa.VARCHAR(length=30),
               nullable=False,
               existing_server_default=sa.text("'OrderItemStatusEnum.PENDING_PAYMENT'::character varying"))
    op.alter_column('order_items', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False,
               existing_server_default=sa.text('now()'))
    op.alter_column('order_items', 'uuid',
               existing_type=sa.UUID(),
               nullable=False,
               existing_server_default=sa.text('gen_random_uuid()'))
    # ### end Alembic commands ###