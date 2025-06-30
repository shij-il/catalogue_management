"""
Utility functions for validating various types of user input.
These functions raise ValidationError on failure, making them suitable for API use.
"""
from datetime import datetime, date

from exception.exceptions import validationerror 
import re

def validate_str(value: str, field_name: str = "Field") -> str:
    """
    Validates that a string input is non-empty and contains allowed characters.
    Allowed characters are letters, numbers, spaces, and common punctuation.

    Args:
        value (str): The string value to validate.
        field_name (str): The descriptive name of the field for error messages.

    Returns:
        str: The stripped and validated string.

    Raises:
        ValidationError: If the value is not a string, is empty, or contains invalid characters.
    """
    if not isinstance(value, str):
        raise ValidationError(f"{field_name} must be a string.")
    if not value.strip(): 
        raise validationerror(f"{field_name} cannot be empty.")
    
    if not re.match(r"^[A-Za-z0-9 .,!?&'\-\(\)]+$", value):
        raise validationerror(
            f"Invalid input for {field_name}! Only letters, numbers, spaces, "
            "and common punctuation (.,!?-&'()) are allowed."
        )
    return value.strip()

def validate_name_str(value: str, field_name: str = "Field") -> str:
    """
    Validates that a name string input is non-empty and contains only letters and spaces.

    Args:
        value (str): The string value to validate.
        field_name (str): The descriptive name of the field for error messages.

    Returns:
        str: The stripped and validated string.

    Raises:
        ValidationError: If the value is not a string, is empty, or contains non-alphabetic characters.
    """
    if not isinstance(value, str):
        raise ValidationError(f"{field_name} must be a string.")
    if not value.strip():
        raise validationerror(f"{field_name} cannot be empty.")
    
    if not re.match(r"^[A-Za-z ]+$", value):
        raise validationerror(f"Invalid input for {field_name}! Only letters and spaces are allowed.")
    return value.strip()

def validate_int(value: any, field_name: str = "Field") -> int:
    """
    Validates that the input can be converted to a positive integer.

    Args:
        value (any): The value to validate (e.g., from request JSON or URL parameter).
        field_name (str): The descriptive name of the field for error messages.

    Returns:
        int: The validated integer.

    Raises:
        ValidationError: If the value cannot be converted to an integer, is empty, or is not positive.
    """
    if value is None or (isinstance(value, str) and not value.strip()):
        raise validationerror(f"{field_name} cannot be empty.")
    try:
        int_value = int(value)
        if int_value <= 0:
            raise validationerror(f"{field_name} must be a positive number.")
        return int_value
    except (ValueError, TypeError):
        raise validationerror(f"Invalid input for {field_name}!. Please enter a valid number.")

def validate_date(date_str: str, field_name: str = "Date") -> date:
    """
    Validates a date string, ensuring it's in YYYY-MM-DD format and converts it to a date object.

    Args:
        date_str (str): The date string to validate.
        field_name (str): The descriptive name of the field for error messages.

    Returns:
        datetime.date: The validated date object.

    Raises:
        ValidationError: If the string is not a valid date or is in the wrong format.
    """
    if not isinstance(date_str, str):
        raise ValidationError(f"{field_name} must be a string.")
    if not date_str.strip():
        raise validationerror(f"{field_name} cannot be empty.")
    try:
     
        input_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        return input_date
    except ValueError:
        raise validationerror(f"Invalid date format for {field_name}!. Please enter the date in YYYY-MM-DD format.")

def validate_status(value: str, field_name: str = "Status") -> str:
    """
    Validates a status string against a list of allowed statuses.

    Args:
        value (str): The status string to validate.
        field_name (str): The descriptive name of the field for error messages.

    Returns:
        str: The validated and normalized (lowercase, stripped) status string.

    Raises:
        ValidationError: If the status is empty or not one of the allowed values.
    """
    valid_statuses = ["active", "inactive", "upcoming", "expired"]
    if not isinstance(value, str):
        raise validationerror(f"{field_name} must be a string.")
    if not value.strip():
        raise validationerror(f"{field_name} cannot be empty.")
    lower_value = value.strip().lower()
    if lower_value not in valid_statuses:
        
        raise validationerror(f"Invalid status for {field_name}!. Please enter one from: ({'/'.join(valid_statuses)}).")
    return lower_value