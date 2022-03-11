from sqlalchemy import (
    MetaData, Table, Column, TIMESTAMP, Integer,
    TEXT
)
from sqlalchemy.sql import func

meta = MetaData()

users = Table(
    'users', meta,
    Column('name', TEXT, nullable=False),
    Column('email', TEXT, nullable=False),
    Column('age', Integer, nullable=True),
    Column('created_at', TIMESTAMP, server_default=func.now(), nullable=False),
    schema='markybox'
)


def create_tables(engine) -> None:
    meta = MetaData()
    logging.info('Create all tables')
    meta.create_all(bind=engine,
                    tables=[users])


def drop_tables(engine) -> None:
    meta = MetaData()
    logging.info('Drop all tables')
    meta.drop_all(bind=engine,
                  tables=[users])


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
