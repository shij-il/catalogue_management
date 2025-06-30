class validationerror(Exception):
    """
    Raised when a validation check fails.

    :param message: Explanation of the validation error
    """
    def __init__(self, message):
        
        super().__init__(f"Validation error : {message}")

class databaseconnectionerror(Exception):
    """
    Raised when a database connection attempt fails.

    :param message: Explanation of the database connection error
    """
    def __init__(self, message):
        
        super().__init__(f"Data connection error : {message}")

