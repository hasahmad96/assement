"""password added

Revision ID: 63d0f3ce806e
Revises: 
Create Date: 2021-06-11 14:17:55.082126

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '63d0f3ce806e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('employee', sa.Column('password_hash', sa.String(length=128), nullable=False))
    op.drop_column('employee', 'pssword_hash')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('employee', sa.Column('pssword_hash', mysql.VARCHAR(length=128), nullable=False))
    op.drop_column('employee', 'password_hash')
    # ### end Alembic commands ###
