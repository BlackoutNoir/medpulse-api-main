"""Make phone_no nullable in medpulse_user

Revision ID: 6cebcbf95de3
Revises: 20f043060688
Create Date: 2024-10-31 20:42:45.873798

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '6cebcbf95de3'
down_revision: Union[str, None] = '20f043060688'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('medpulse_user', 'phone_no',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('medpulse_user', 'phone_no',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
