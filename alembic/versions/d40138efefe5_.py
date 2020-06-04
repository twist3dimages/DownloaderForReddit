"""empty message

Revision ID: d40138efefe5
Revises: cc433ec81ed6
Create Date: 2020-05-28 12:46:52.904051

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd40138efefe5'
down_revision = 'cc433ec81ed6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reddit_object_list', sa.Column('lock_settings', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('reddit_object_list', 'lock_settings')
    # ### end Alembic commands ###