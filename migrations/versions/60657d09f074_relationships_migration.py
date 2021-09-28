"""Relationships Migration

Revision ID: 60657d09f074
Revises: 8745f694ce0b
Create Date: 2021-09-27 20:08:32.115974

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '60657d09f074'
down_revision = '8745f694ce0b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone_number', sa.VARCHAR(length=11), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone_number')
    # ### end Alembic commands ###
