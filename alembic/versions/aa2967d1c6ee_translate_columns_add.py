"""translate columns add

Revision ID: aa2967d1c6ee
Revises: 78b8f49ec3e3
Create Date: 2022-04-24 17:47:22.813517

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa2967d1c6ee'
down_revision = '78b8f49ec3e3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('holidays', sa.Column('hn_uz', sa.String(), nullable=True))
    op.add_column('holidays', sa.Column('hn_ua', sa.String(), nullable=True))
    op.add_column('holidays', sa.Column('hn_es', sa.String(), nullable=True))
    op.add_column('holidays', sa.Column('hn_fr', sa.String(), nullable=True))
    op.drop_column('holidays', 'es_ru')
    op.drop_column('holidays', 'uz_ru')
    op.drop_column('holidays', 'fr_ru')
    op.drop_column('holidays', 'ua_ru')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('holidays', sa.Column('ua_ru', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('holidays', sa.Column('fr_ru', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('holidays', sa.Column('uz_ru', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('holidays', sa.Column('es_ru', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('holidays', 'hn_fr')
    op.drop_column('holidays', 'hn_es')
    op.drop_column('holidays', 'hn_ua')
    op.drop_column('holidays', 'hn_uz')
    # ### end Alembic commands ###
