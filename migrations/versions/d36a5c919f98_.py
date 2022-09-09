"""empty message

Revision ID: d36a5c919f98
Revises: 
Create Date: 2022-09-09 13:36:38.686727

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd36a5c919f98'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'meme_tag', 'meme', ['meme_id'], ['id'])
    op.create_foreign_key(None, 'meme_tag', 'tag', ['tag_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'meme_tag', type_='foreignkey')
    op.drop_constraint(None, 'meme_tag', type_='foreignkey')
    # ### end Alembic commands ###