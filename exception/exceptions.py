"""
Custom exception classes for the Catalogue Management System.
Adds logging for each exception raised.
"""

import logging


logger = logging.getLogger(__name__)

class validationerror(Exception):
    """
    Exception raised when an input validation check fails.
    Logs the validation failure message.
    """
    def __init__(self, message: str):
        full_message = f"Validation Error: {message}"
        logger.warning(full_message)
        super().__init__(full_message)

class databaseconnectionerror(Exception):
    """
    Exception raised when a database connection cannot be established or fails.
    Logs the DB failure message.
    """
    def __init__(self, message: str):
        full_message = f"Database Connection Error: {message}"
        logger.error(full_message)
        super().__init__(full_message)
