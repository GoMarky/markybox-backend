import yaml
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, 'config.yml'), 'r') as stream:
    config = yaml.load(stream)

DSN = 'postgres://{user}:{password}@{host}:{port}/{database}'
DB_CONFIG = config.get('postgres')
LOGGER_CONFIG = config.get('logger')
APP = config.get('app')
