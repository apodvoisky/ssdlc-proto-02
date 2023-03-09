"""Initial

Revision ID: 9a3a7d6645ef
Revises: fbabbf594c20
Create Date: 2023-03-09 18:38:13.694873

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a3a7d6645ef'
down_revision = 'fbabbf594c20'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('second_name', sa.String(), nullable=True),
    sa.Column('sur_name', sa.String(), nullable=True),
    sa.Column('cell_phone', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_customer_id'), 'customer', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_customer_id'), table_name='customer')
    op.drop_table('customer')
    # ### end Alembic commands ###
