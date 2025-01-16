from loguru import logger
import sys

logger.remove()
logger.add(
    sys.stdout,
    format='<level>{level: <5}</level> | {message}',
    level='DEBUG'
)