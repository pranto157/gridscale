"""initial

Revision ID: 39d319bcf53c
Revises:
Create Date: 2023-11-23 20:12:24.033192

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "39d319bcf53c"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Define the ENUM type explicitly with a name
    op.create_table(
        "cities",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("city_uuid", sa.String(36), nullable=False, unique=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("geo_location_latitude", sa.Float(), nullable=False),
        sa.Column("geo_location_longitude", sa.Float(), nullable=False),
        sa.Column("beauty", sa.String(36), nullable=False),
        sa.Column("population", sa.BigInteger(), nullable=False),
        sa.Column("allied_cities", sa.JSON()),
        # Add other columns as needed based on your model
    )

    # Creating indexes
    op.create_index("idx_city_uuid", "cities", ["city_uuid"])
    op.create_index("idx_name", "cities", ["name"])


def downgrade() -> None:
    pass
