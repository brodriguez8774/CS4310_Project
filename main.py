"""
Core/Start of program.
"""

from resources import logging


# Initialize logging.
logger = logging.get_logger(__name__)


# Core program here.
logger.info('Hello World.')


# Program termination and clean up.
logger.info('Terminating program.')
