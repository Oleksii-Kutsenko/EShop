"""empty message

Revision ID: 7546466e709f
Revises: 
Create Date: 2023-01-30 10:23:36.170228

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7546466e709f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('order_status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_status_name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('place_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('place_type_name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('place_type_name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('last_seen', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('status_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['status_id'], ['order_status.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('place',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('taking_date', sa.DateTime(), nullable=False),
    sa.Column('release_date', sa.DateTime(), nullable=False),
    sa.Column('place_type_id', sa.Integer(), nullable=False),
    sa.Column('place_class', sa.Integer(), nullable=False),
    sa.Column('price', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['place_type_id'], ['place_type.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('association',
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('place_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], ),
    sa.ForeignKeyConstraint(['place_id'], ['place.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('association')
    op.drop_table('place')
    op.drop_table('order')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('place_type')
    op.drop_table('order_status')
    # ### end Alembic commands ###
