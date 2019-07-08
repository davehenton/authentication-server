"""create users table

Revision ID: 8000b7a6eb14
Revises: 
Create Date: 2019-07-03 17:50:56.158462

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '8000b7a6eb14'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column("id", sa.Integer, autoincrement=True, primary_key=True),
        sa.Column("user_client", sa.Text, nullable=False, unique=True),
        sa.Column("user_secret", sa.Text, nullable=False),
        sa.Column("salt", sa.Text, nullable=False),
        sa.Column("creation_time", sa.DateTime, nullable=False),
        sa.Column("updated_time", sa.DateTime, nullable=True),
        sa.Column("remarks", sa.Text, nullable=True)
    )

def downgrade():
    op.drop_table('users')
