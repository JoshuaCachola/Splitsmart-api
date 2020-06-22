"""add is_settled to expenses

Revision ID: bfa080d24947
Revises: b0c74e8122ca
Create Date: 2020-06-20 21:17:50.170752

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bfa080d24947'
down_revision = 'b0c74e8122ca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('expenses', sa.Column('is_settled', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('expenses', 'is_settled')
    # ### end Alembic commands ###