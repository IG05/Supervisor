#tasks
from celery import Celery
import logging

celery = Celery(
    'tasks',
    broker='redis://host.docker.internal:6379/0',
    backend='redis://host.docker.internal:6379/0'
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@celery.task
def add(x, y):
    result = x + y
    logger.info(f"Running task add({x}, {y}) = {result}")
    return result
