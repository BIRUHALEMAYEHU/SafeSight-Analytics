"""add person photo metadata

Revision ID: a1b2c3d4e5f6
Revises: e0a337ae61a8
Create Date: 2025-12-30 12:45:00.000000
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "a1b2c3d4e5f6"
down_revision = "e0a337ae61a8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("persons_of_interest", sa.Column("photo_mime", sa.String(length=255), nullable=True))
    op.add_column("persons_of_interest", sa.Column("photo_size", sa.Integer(), nullable=True))
    op.add_column("persons_of_interest", sa.Column("photo_checksum", sa.String(length=255), nullable=True))
    op.add_column("persons_of_interest", sa.Column("photo_uploaded_at", sa.DateTime(), nullable=True))


def downgrade() -> None:
    op.drop_column("persons_of_interest", "photo_uploaded_at")
    op.drop_column("persons_of_interest", "photo_checksum")
    op.drop_column("persons_of_interest", "photo_size")
    op.drop_column("persons_of_interest", "photo_mime")
