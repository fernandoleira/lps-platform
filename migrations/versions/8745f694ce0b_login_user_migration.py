"""Login user migration

Revision ID: 8745f694ce0b
Revises: 2268d72d8102
Create Date: 2021-09-15 20:27:06.117539

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8745f694ce0b'
down_revision = '2268d72d8102'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('pswd_hash', sa.String(), nullable=False))
    op.drop_column('users', 'password')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password', postgresql.BYTEA(), autoincrement=False, nullable=False))
    op.drop_column('users', 'pswd_hash')
    # ### end Alembic commands ###