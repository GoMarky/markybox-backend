from sqlalchemy import (
    MetaData, Table, Column, TIMESTAMP,
    TEXT, ForeignKeyConstraint, Integer, UniqueConstraint, ARRAY
)
from sqlalchemy.sql import func

meta = MetaData()

users = Table(
    'users', meta,
    Column('client_id', Integer, primary_key=True, nullable=False),
    Column('client_name', TEXT, nullable=False, unique=False),
    Column('client_email', TEXT, nullable=False, unique=True),
    Column('password', TEXT, nullable=False, unique=False),

    Column('created_ts', TIMESTAMP, server_default=func.now(), nullable=False),
    Column('updated_ts', TIMESTAMP, server_default=func.now(), nullable=False),
    schema='swentech'
)

sessions = Table(
    'sessions', meta,
    Column('client_id', Integer, nullable=False),
    Column('session_id', TEXT, nullable=False, unique=True),
    Column('created_ts', TIMESTAMP, server_default=func.now(), nullable=False),

    ForeignKeyConstraint(['client_id'], [users.c.client_id],
                         name='sessions_client_id_fkey',
                         ondelete='CASCADE'),
    UniqueConstraint('client_id', 'session_id', name='cl_sess'),
    schema='swentech'
)

categories = Table(
    'categories', meta,
    Column('client_id', Integer, nullable=False),
    Column('category_id', Integer, primary_key=True, nullable=False),
    Column('category_slug', TEXT, nullable=False, unique=True),

    Column('created_ts', TIMESTAMP, server_default=func.now(), nullable=False),
    Column('updated_ts', TIMESTAMP, server_default=func.now(), nullable=False),

    ForeignKeyConstraint(['client_id'], [users.c.client_id],
                         name='created_by_client_id_fkey',
                         ondelete=None),
    UniqueConstraint('client_id', 'category_id', name='cl_category_created'),
    schema='swentech'
)

categories_lang = Table(
    'categories_lang', meta,
    Column('category_lang_id', Integer, primary_key=True, nullable=False),
    Column('category_id', Integer, nullable=False),
    Column('name_ru', TEXT, nullable=False, unique=False),
    Column('name_en', TEXT, nullable=False, unique=False),
    Column('name_fr', TEXT, nullable=False, unique=False),
    Column('created_ts', TIMESTAMP, server_default=func.now(), nullable=False),
    Column('updated_ts', TIMESTAMP, server_default=func.now(), nullable=False),

    ForeignKeyConstraint(['category_id'], [categories.c.category_id],
                         name='category_id_fkey',
                         ondelete="CASCADE"),
    UniqueConstraint('category_id', 'category_lang_id', name='cl_category'),
    schema='swentech'
)

tags = Table(
    'tags', meta,
    Column('client_id', Integer, nullable=False),
    Column('tag_id', Integer, primary_key=True, nullable=False),
    Column('tag_slug', TEXT, nullable=False, unique=True),

    Column('created_ts', TIMESTAMP, server_default=func.now(), nullable=False),
    Column('updated_ts', TIMESTAMP, server_default=func.now(), nullable=False),

    ForeignKeyConstraint(['client_id'], [users.c.client_id],
                         name='client_id_fkey',
                         ondelete=None),
    schema='swentech'
)

tags_lang = Table(
    'tags_lang', meta,
    Column('tag_lang_id', Integer, primary_key=True, nullable=False),
    Column('tag_id', Integer, nullable=False),
    Column('name_ru', TEXT, nullable=False, unique=False),
    Column('name_en', TEXT, nullable=False, unique=False),
    Column('name_fr', TEXT, nullable=False, unique=False),
    Column('created_ts', TIMESTAMP, server_default=func.now(), nullable=False),
    Column('updated_ts', TIMESTAMP, server_default=func.now(), nullable=False),

    ForeignKeyConstraint(['tag_id'], [tags.c.tag_id],
                         name='tag_id_fkey',
                         ondelete="CASCADE"),
    UniqueConstraint('tag_id', 'tag_lang_id', name='cl_tag'),
    schema='swentech'
)

posts = Table(
    'posts', meta,
    Column('client_id', Integer, nullable=False),
    Column('category_id', Integer, nullable=False),

    Column('post_id', Integer, primary_key=True, nullable=False),
    Column('post_slug', TEXT, nullable=False, unique=True),

    Column('post_url', TEXT, nullable=False, unique=True),
    Column('post_featured_image', TEXT, nullable=False, unique=False),
    Column('post_status', Integer, nullable=False, unique=True),

    Column('post_tags_id', ARRAY(Integer), nullable=False, unique=True),

    Column('created_ts', TIMESTAMP, server_default=func.now(), nullable=False),
    Column('updated_ts', TIMESTAMP, server_default=func.now(), nullable=False),

    ForeignKeyConstraint(['client_id'], [users.c.client_id],
                         name='client_id_fkey',
                         ondelete=None),

    ForeignKeyConstraint(['category_id'], [categories.c.category_id],
                         name='category_id_fkey',
                         ondelete=None),
    schema='swentech'
)

posts_lang = Table(
    'posts_lang', meta,
    Column('post_id', Integer,  nullable=False),
    Column('post_lang_id', Integer, primary_key=True, nullable=False),
    Column('text_ru', TEXT, nullable=False, unique=False),
    Column('text_en', TEXT, nullable=False, unique=False),
    Column('text_fr', TEXT, nullable=False, unique=False),

    Column('title_ru', TEXT, nullable=False, unique=False),
    Column('title_en', TEXT, nullable=False, unique=False),
    Column('title_fr', TEXT, nullable=False, unique=False),

    Column('created_ts', TIMESTAMP, server_default=func.now(), nullable=False),
    Column('updated_ts', TIMESTAMP, server_default=func.now(), nullable=False),

    ForeignKeyConstraint(['post_lang_id'], [posts.c.post_id],
                         name='post_id_fkey',
                         ondelete="CASCADE"),
    UniqueConstraint('post_id', 'post_lang_id', name='post_id'),
    schema='swentech'
)


def create_tables(engine) -> None:
    meta = MetaData()
    logging.info('Create all tables')
    meta.create_all(bind=engine,
                    tables=[users, sessions, categories, categories_lang, tags, tags_lang, posts, posts_lang])


def drop_tables(engine) -> None:
    meta = MetaData()
    logging.info('Drop all tables')
    meta.drop_all(bind=engine,
                  tables=[users, sessions, categories, categories_lang, tags, tags_lang, posts, posts_lang])


if __name__ == '__main__':
    from configuration import DB_CONFIG, DSN
    from sqlalchemy import create_engine
    import logging

    logging.basicConfig(
        level=logging.DEBUG,
        format='[{asctime}][{levelname}] - {name}: {message}', style='{')

    engine = create_engine(DSN.format(**DB_CONFIG))
    drop_tables(engine)
    create_tables(engine)
