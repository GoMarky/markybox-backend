import os
import sys
import logging
import psycopg2

from configuration import DB_CONFIG, DSN

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MIGRATIONS_DIR = os.path.join(BASE_DIR, 'sql/')
UTILS = ['bootstrap', 'migration']


def bootstrap(db_config: dict) -> None:
    """
    Function for creating all needed for work tables
    in already created database.

    :param db_config: database configuration
    """

    logging.info('Run bootstrap')
    try:
        with psycopg2.connect(dsn=DSN.format(**db_config)) as connection:
            logging.info('Connected to PostgresDB')
            with connection.cursor() as cursor:
                with open(MIGRATIONS_DIR + '002_tables.sql', 'r') as bs:
                    cursor.execute(bs.read())
    except psycopg2.OperationalError as e:
        sys.exit(f'System error: {e}')
    logging.info('Bootstrap is finished')


def migrations(db_config: dict) -> None:
    """
    Function for migrate database

    :param db_config:  database configuration
    :return:
    """

    logging.info(f'Run sql')
    pass


if __name__ == '__main__':
    # Set logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='[{asctime}][{levelname}] - {name}: {message}', style='{'
    )

    # Set configurations
    db_config = DB_CONFIG

    if len(sys.argv) > 1 and sys.argv[1] != 'help':
        util = sys.argv[1]
        if util in UTILS and util == 'bootstrap':
            bootstrap(db_config=db_config)

        elif util in UTILS and util == 'migration':
            migrations(db_config=db_config)

        else:
            print(f'Unknown util {util}')
            print('Usage main.py {util} ')
            print('Module: %s' % (' | '.join(UTILS)))

    else:
        print('Set util')
        print('Usage main.py {util} ')
        print('Module: %s' % (' | '.join(UTILS)))
