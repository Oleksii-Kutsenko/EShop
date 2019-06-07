"""empty message

Revision ID: 15f8d89facc0
Revises: fe57ff9c1bdc
Create Date: 2019-06-07 20:40:48.942776

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '15f8d89facc0'
down_revision = 'fe57ff9c1bdc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'place_type', ['place_type_name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'place_type', type_='unique')
    # ### end Alembic commands ###