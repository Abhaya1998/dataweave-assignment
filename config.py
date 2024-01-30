import os

from dotenv import load_dotenv
load_dotenv()

import logging as logger

RABBITMQ_BROKER_URL = os.environ['RABBITMQ_BROKER_URL']
TASK_QUEUE = os.environ['TASK_QUEUE']
POSTGRES_URL = os.environ['POSTGRES_URL']
TABLE_NAME = 'products'