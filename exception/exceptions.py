"""
Custom exception classes for the Catalogue Management System.
"""
class validationerror(Exception):
    """
    Exception raised when an input validation check fails.
    """
    def __init__(self, message: str):
        
        super().__init__(f"Validation Error: {message}") 

class databaseconnectionerror(Exception):
    """
    Exception raised when a database connection cannot be established or fails.
    """
    def __init__(self, message: str):
        super().__init__(f"Database Connection Error: {message}")

