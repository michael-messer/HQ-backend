"""empty message

Revision ID: 12044db60778
Revises: ead656e5233c
Create Date: 2022-05-31 05:58:38.835076

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12044db60778'
down_revision = 'ead656e5233c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('companies', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'companies', 'users', ['user_id'], ['id'])
    op.drop_column('companies', 'title')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('companies', sa.Column('title', sa.VARCHAR(length=128), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'companies', type_='foreignkey')
    op.drop_column('companies', 'user_id')
    # ### end Alembic commands ###