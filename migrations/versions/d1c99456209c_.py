"""empty message

Revision ID: d1c99456209c
Revises: 1b0d6653b1be
Create Date: 2023-09-27 13:21:07.909556

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd1c99456209c'
down_revision = '1b0d6653b1be'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('order_dish_association',
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('dish_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['dish_id'], ['dishes.id'], ),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], )
    )
    with op.batch_alter_table('dishes', schema=None) as batch_op:
        batch_op.drop_constraint('dishes_ibfk_1', type_='foreignkey')
        batch_op.drop_column('order_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('dishes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('order_id', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('dishes_ibfk_1', 'orders', ['order_id'], ['id'])

    op.drop_table('order_dish_association')
    # ### end Alembic commands ###
