"""empty message

Revision ID: fe57ff9c1bdc
Revises: c6a7f00bdfd5
Create Date: 2019-06-07 17:11:42.926535

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'fe57ff9c1bdc'
down_revision = 'c6a7f00bdfd5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('is_admin', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'is_admin')
    # ### end Alembic commands ###