from __init__ import make_celery
import logging

celery = make_celery()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@celery.task
def add(x, y):
    result = x + y
    logger.info(f"Running task add({x}, {y}) = {result}")
    return result
