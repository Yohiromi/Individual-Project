"""empty message

Revision ID: 8aaae6e8cd39
Revises: 1f914cdf1566
Create Date: 2022-04-24 17:33:14.024481

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '8aaae6e8cd39'
down_revision = '1f914cdf1566'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('wenjuan_exts', 'create_time')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('wenjuan_exts', sa.Column('create_time', mysql.DATETIME(), nullable=True))
    # ### end Alembic commands ###
