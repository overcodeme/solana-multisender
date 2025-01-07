from loguru import logger
import sys

logger.remove()
logger.add(
    sys.stdout,
    format='<cyan>{time:HH:mm:ss}</cyan> | <level>{level: <8}</level> | — Wallet: {extra[address]} | {message}',
    level='DEBUG'
)