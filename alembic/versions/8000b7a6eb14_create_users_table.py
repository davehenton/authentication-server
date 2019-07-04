"""create users table

Revision ID: 8000b7a6eb14
Revises: 
Create Date: 2019-07-03 17:50:56.158462

"""
import sqlalchemy as sa
from alembic import op

from sqlalchemy.schema import Sequence, CreateSequence, DropSequence

# revision identifiers, used by Alembic.
revision = '8000b7a6eb14'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    users_table = op.create_table(
        'users',
        sa.Column("id", sa.Integer, autoincrement=True, primary_key=True),
        sa.Column("user_client", sa.Text, nullable=False, unique=True),
        sa.Column("user_secret", sa.Text, nullable=False),
        sa.Column("salt", sa.Text, nullable=False),
        sa.Column("creation_time", sa.DateTime, nullable=False),
        sa.Column("updated_time", sa.DateTime, nullable=True),
        sa.Column("remarks", sa.Text, nullable=True)
    )
    op.bulk_insert(users_table, [
        {
            'user_client': 'system',
            'user_secret': 'e5907bb05e32124f1ded6ef152d81b40b63da01d2d2ed41e61af57d4cda2f797',
            'salt': 'e846d6749d6b11e9abd66030d474b104',
            'creation_time': '2019-07-03 17:23:59.556232'
        }
    ], multiinsert=False)

def downgrade():
    op.drop_table('users')
