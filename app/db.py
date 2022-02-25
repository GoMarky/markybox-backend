from sqlalchemy import (
    MetaData, Table, Column, TIMESTAMP,
    TEXT
)
from sqlalchemy.sql import func

meta = MetaData()

sessions = Table(
    'sessions', meta,
    Column('author', TEXT, nullable=False),
    Column('author', TEXT, nullable=True),
    Column('session_id', TEXT, nullable=False, unique=True),
    Column('created_ts', TIMESTAMP, server_default=func.now(), nullable=False),
    schema='markybox'
)


def create_tables(engine) -> None:
    meta = MetaData()
    logging.info('Create all tables')
    meta.create_all(bind=engine,
                    tables=[sessions])


def drop_tables(engine) -> None:
    meta = MetaData()
    logging.info('Drop all tables')
    meta.drop_all(bind=engine,
                  tables=[sessions])


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
