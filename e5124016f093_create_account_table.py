from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5124016f093'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement = True),
        sa.Column('first_name', sa.String(45), nullable=False),
        sa.Column('last_name', sa.String(45), nullable=False),
        sa.Column('login', sa.String(45), nullable=False),
        sa.Column('password', sa.String(45), nullable=False),
        sa.Column('role', sa.Enum("USER", "SUPERUSER"), default='USER', nullable=False),
    )

    op.create_table(
        'artist',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement = True),
        sa.Column('first_name', sa.String(45), nullable=False),
        sa.Column('last_name', sa.String(45), nullable=False),
        sa.Column('raiting', sa.Enum("1", "2", "3", "4", "5"), nullable=False),
    )

    op.create_table(
        'category',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement = True),
        sa.Column('name', sa.String(45), nullable=False),
    )
    op.create_table(
        'song',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('lyrics', sa.String(10000), nullable=False),
        sa.Column('raiting', sa.Enum("1", "2", "3", "4", "5"), nullable=False),
        sa.Column('duration', sa.Float(2), nullable=False),
        sa.Column('category_id', sa.Integer, sa.ForeignKey("category.id"), nullable=False, primary_key=True),
    )
    op.create_table(
        'playlist',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('status', sa.Enum("PRIVATE", "PUBLIC"), nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey("user.id"), nullable=False, primary_key=True),
        sa.Column('artist_id', sa.Integer, sa.ForeignKey("artist.id"), nullable=False, primary_key=True),
        sa.Column('song_id', sa.Integer, sa.ForeignKey("song.id"), nullable=False, primary_key=True),
    )

    op.create_table(
        'album',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('released', sa.DATETIME, nullable=False),
        sa.Column('artist_id', sa.Integer, sa.ForeignKey("artist.id"), nullable=False, primary_key=True),
        sa.Column('song_id', sa.Integer, sa.ForeignKey("song.id"), nullable=False, primary_key=True),

    )


def downgrade() -> None:
    op.drop_table('user')
    op.drop_table('artist')
    op.drop_table('category')
    op.drop_table('playlist')
    op.drop_table('song')
    op.drop_table('album')