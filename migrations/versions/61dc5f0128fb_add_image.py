"""add image

Revision ID: 61dc5f0128fb
Revises: 7445121ea388
Create Date: 2022-04-25 18:21:48.394696

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61dc5f0128fb'
down_revision = '7445121ea388'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('recipe', sa.Column('image', sa.Text(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('recipe', 'image')
    # ### end Alembic commands ###
