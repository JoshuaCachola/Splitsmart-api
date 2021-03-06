"""added users friends join table

Revision ID: 4a4fccf5e86c
Revises: 31ade991f60b
Create Date: 2020-06-21 14:53:18.950304

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a4fccf5e86c'
down_revision = '31ade991f60b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users_friends',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('friend_id', sa.Integer(), nullable=False),
    sa.Column('users_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['friend_id'], ['friends.id'], ),
    sa.ForeignKeyConstraint(['users_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_friends')
    # ### end Alembic commands ###
