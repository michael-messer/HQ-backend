"""empty message

Revision ID: aee50b049219
Revises: 12044db60778
Create Date: 2022-05-31 08:29:11.065260

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aee50b049219'
down_revision = '12044db60778'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('companies', 'description',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('companies', 'description',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    # ### end Alembic commands ###