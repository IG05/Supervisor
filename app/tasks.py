#tasks
from celery import Celery
import logging
import os

REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')


celery = Celery(
    'tasks',
    broker=REDIS_URL,
    backend=REDIS_URL
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@celery.task
def add(x, y):
    result = x + y
    logger.info(f"Running task add({x}, {y}) = {result}")
    return result
