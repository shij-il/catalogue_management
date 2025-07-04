"""
Utility for establishing database connections using config file.
Adds logging for connection attempts and failures.
"""

import mysql.connector
from configparser import ConfigParser
from exception.exceptions import databaseconnectionerror
import logging
import logging.config
import os


if not os.path.exists('logs'):
    os.makedirs('logs')

logging.config.fileConfig('config/catalogue_logging.ini')
logger = logging.getLogger(__name__)

def get_connection():
    """
    Connects to the MySQL database using configuration from config file.

    :return: MySQL connection object.
    :raises databaseconnectionerror: If connection fails.
    """
    config = ConfigParser()
    config.read("config/db_connection_config.ini")
    try:
        conn = mysql.connector.connect(
            host=config["mysql"]["host"],
            user=config["mysql"]["user"],
            password=config["mysql"]["password"],
            database=config["mysql"]["database"]
        )
        logger.info("Database connection established successfully.")
        return conn
    except mysql.connector.Error as err:
        logger.error(f"Database connection failed: {err}")
        raise databaseconnectionerror(f"Database connection failed: {err}")
