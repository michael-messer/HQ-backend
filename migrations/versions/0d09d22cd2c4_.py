"""empty message

Revision ID: 0d09d22cd2c4
Revises: 81204c3e8841
Create Date: 2022-06-07 11:14:13.584771

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d09d22cd2c4'
down_revision = '81204c3e8841'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('talents', sa.Column('uuid', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('talents', 'uuid')
    # ### end Alembic commands ###
