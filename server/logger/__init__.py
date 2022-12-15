from .logger import LogConfig
from logging.config import dictConfig
import logging

dictConfig(LogConfig().dict())
logger = logging.getLogger("mycoolapp")