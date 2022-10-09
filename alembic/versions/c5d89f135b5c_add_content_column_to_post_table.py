"""Add Content Column To Post Table

Revision ID: c5d89f135b5c
Revises: 704fdd1d0200
Create Date: 2022-10-06 11:42:08.941517

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5d89f135b5c'
down_revision = '704fdd1d0200'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
