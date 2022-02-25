import logging
from aiohttp import web
from app.app import create_app
from configuration import APP, LOGGER_CONFIG


def setup_logging(config: dict):
    logging.basicConfig(
        level=config['logger_level'],
        format=config['format'],
        style=config['style'],
    )


def run_app(port: int):
    app = create_app()
    web.run_app(app, port=port)


if __name__ == '__main__':
    setup_logging(config=LOGGER_CONFIG)
    run_app(port=APP['port'])
