"""
Utility for establishing database connections using config file.
"""
import mysql.connector
from configparser import ConfigParser
from exception.exceptions import databaseconnectionerror

def get_connection():
    """
    Connects to the MySQL database using configuration from config file.

    :return: MySQL connection object.
    :raises databaseconnectionerror: If connection fails.
    """
    config = ConfigParser()
    config.read("config/db_connection_config.ini")
    try:
        return mysql.connector.connect(
        host=config["mysql"] ["host"],
        user=config["mysql"] ["user"],
        password=config["mysql"] ["password"],
        database=config["mysql"] ["database"]
        )
    except mysql.connector.Error as err:
        raise databaseconnectionerror(f"database connection failed : {err}")