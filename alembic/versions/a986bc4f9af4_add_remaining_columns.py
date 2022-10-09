"""Add Remaining Columns

Revision ID: a986bc4f9af4
Revises: 1a6bf7f2e4dd
Create Date: 2022-10-06 14:08:46.383800

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a986bc4f9af4'
down_revision = '1a6bf7f2e4dd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("published", sa.Boolean(), nullable=False, 
        server_default='TRUE'))
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True), 
        nullable=False, server_default=sa.text("now()")),)
    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
