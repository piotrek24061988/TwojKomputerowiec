"""empty message

Revision ID: 34905c866679
Revises: 
Create Date: 2021-05-14 12:07:07.549423

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34905c866679'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('aktualnosc',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tytul', sa.String(length=100), nullable=False),
    sa.Column('data', sa.DateTime(), nullable=False),
    sa.Column('tresc', sa.Text(), nullable=False),
    sa.Column('zdjecie', sa.String(length=20), nullable=True),
    sa.Column('videoUrl', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('galeria',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tytul', sa.String(length=100), nullable=False),
    sa.Column('data', sa.DateTime(), nullable=False),
    sa.Column('zdjecie', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('produkt',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tytul', sa.String(length=100), nullable=False),
    sa.Column('data', sa.DateTime(), nullable=False),
    sa.Column('tresc', sa.Text(), nullable=False),
    sa.Column('zdjecie', sa.String(length=20), nullable=True),
    sa.Column('ilosc', sa.Integer(), nullable=True),
    sa.Column('cena', sa.Float(), nullable=True),
    sa.Column('cyfrowy', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('uzytkownik',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('zdjecie', sa.String(length=20), nullable=False),
    sa.Column('haslo', sa.String(length=60), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tytul', sa.String(length=100), nullable=False),
    sa.Column('data', sa.DateTime(), nullable=False),
    sa.Column('tresc', sa.Text(), nullable=False),
    sa.Column('uzytkownik_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['uzytkownik_id'], ['uzytkownik.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post')
    op.drop_table('uzytkownik')
    op.drop_table('produkt')
    op.drop_table('galeria')
    op.drop_table('aktualnosc')
    # ### end Alembic commands ###