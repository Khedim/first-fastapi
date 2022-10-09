"""Create Post Table

Revision ID: 704fdd1d0200
Revises: 
Create Date: 2022-10-06 11:15:07.513960

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '704fdd1d0200'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("posts", sa.Column("id", sa.Integer(), nullable=False, primary_key=True), 
    sa.Column("title", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
