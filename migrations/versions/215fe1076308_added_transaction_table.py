"""added transaction table

Revision ID: 215fe1076308
Revises: 4a4fccf5e86c
Create Date: 2020-06-21 15:15:03.442750

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '215fe1076308'
down_revision = '4a4fccf5e86c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('transactions',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('paid_on', sa.DateTime(), nullable=True),
    sa.Column('is_settled', sa.Boolean(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transactions')
    # ### end Alembic commands ###
