"""Add content column to post table

Revision ID: 91197addc52c
Revises: 2ea62e695c20
Create Date: 2024-01-31 13:36:27.000121

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '91197addc52c'
down_revision: Union[str, None] = '2ea62e695c20'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
