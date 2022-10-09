"""Add Foreign_key To Posts Table

Revision ID: 1a6bf7f2e4dd
Revises: 3a804ba0637a
Create Date: 2022-10-06 13:53:14.219952

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a6bf7f2e4dd'
down_revision = '3a804ba0637a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer, nullable=False))
    op.create_foreign_key("post_users_fk", source_table="posts", referent_table="users", 
                        local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
