"""empty message

Revision ID: 969a287e3ba1
Revises: faac96d04ebe
Create Date: 2022-05-27 02:42:06.490533

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '969a287e3ba1'
down_revision = 'faac96d04ebe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('appliedjobs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('job_id', sa.Integer(), nullable=False),
    sa.Column('applied_at', sa.DateTime(), nullable=False),
    sa.Column('on_shortlist', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('companies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=False),
    sa.Column('description', sa.String(length=128), nullable=False),
    sa.Column('region', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('account_manager_name', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('companies')
    op.drop_table('appliedjobs')
    # ### end Alembic commands ###