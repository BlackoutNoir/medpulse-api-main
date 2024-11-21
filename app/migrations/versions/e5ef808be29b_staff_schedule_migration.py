"""staff schedule migration

Revision ID: e5ef808be29b
Revises: e36a0ba03581
Create Date: 2024-11-17 16:55:36.837196

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'e5ef808be29b'
down_revision: Union[str, None] = 'e36a0ba03581'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('schedule',
    sa.Column('uid', sa.UUID(), nullable=False),
    sa.Column('staff_uid', sa.Uuid(), nullable=False),
    sa.Column('shift_start', sa.DateTime(), nullable=False),
    sa.Column('shift_end', sa.DateTime(), nullable=False),
    sa.Column('day_of_week', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('location', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('notes', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.ForeignKeyConstraint(['staff_uid'], ['staff.uid'], ),
    sa.PrimaryKeyConstraint('uid')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('schedule')
    # ### end Alembic commands ###
