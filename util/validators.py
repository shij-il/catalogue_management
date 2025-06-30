"""
Utility functions to validate user input.
"""
from datetime import datetime, date
from exception.exceptions import validationerror 
import re

def validate_str(value: str, field_name: str = "Field") -> str:
    """
    Validates that input is a non-empty string with allowed characters.

    :param value: The string value to validate.
    :param field_name: Name of the field for error messages.
    :return: Validated string.
    :raises ValidationError: If validation fails.
    """
    if not isinstance(value, str):
        raise validationerror(f"{field_name} must be a string.")
    if not value.strip():
        raise validationerror(f"{field_name} cannot be empty.")
    
    if not re.match(r"^[A-Za-z0-9 .,!?&'\-\(\)]+$", value): 
        raise validationerror(f"Invalid input for {field_name}! Only letters, numbers, spaces, and common punctuation (.,!?-&'()) are allowed.")
    return value.strip()

def validate_name_str(value: str, field_name: str = "Field") -> str:
    """
    Validates that input is a non-empty string with only letters and spaces.

    :param value: The string value to validate.
    :param field_name: Name of the field for error messages.
    :return: Validated string.
    :raises ValidationError: If validation fails.
    """
    if not isinstance(value, str):
        raise validationerror(f"{field_name} must be a string.")
    if not value.strip():
        raise validationerror(f"{field_name} cannot be empty.")
    if not re.match(r"^[A-Za-z ]+$", value):
        raise validationerror(f"Invalid input for {field_name}! Only letters and spaces are allowed.")
    return value.strip()

def validate_int(value: any, field_name: str = "Field") -> int:
    """
    Validates integer input.

    :param value: The value to validate.
    :param field_name: Name of the field for error messages.
    :return: Validated integer.
    :raises ValidationError: If validation fails.
    """
    if value is None or value == '': 
        raise validationerror(f"{field_name} cannot be empty.")
    try:
        int_value = int(value)
        if int_value <= 0:
            raise validationerror(f"{field_name} must be a positive integer.")
        return int_value
    except (ValueError, TypeError):
        raise validationerror(f"Invalid input for {field_name}!. Enter a valid number.")

def validate_date(date_str: str, field_name: str = "Date") -> date:
    """
    Validates date input in YYYY-MM-DD format.

    :param date_str: The date string to validate.
    :param field_name: Name of the field for error messages.
    :return: Validated date object.
    :raises ValidationError: If validation fails.
    """
    if not isinstance(date_str, str):
        raise validationerror(f"{field_name} must be a string.")
    if not date_str.strip():
        raise validationerror(f"{field_name} cannot be empty.")
    try:
        input_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        return input_date 
    except ValueError:
        raise validationerror(f"Invalid date format for {field_name}!. Enter the date in (YYYY-MM-DD) format.")

def validate_status(value: str, field_name: str = "Status") -> str:
    """
    Validates if the status input is valid.

    :param value: The status string to validate.
    :param field_name: Name of the field for error messages.
    :return: Validated status string.
    :raises ValidationError: If validation fails.
    """
    valid_status = ["active", "inactive", "upcoming", "expired"]
    if not isinstance(value, str):
        raise validationerror(f"{field_name} must be a string.")
    if not value.strip():
        raise validationerror(f"{field_name} cannot be empty.")
    lower_value = value.strip().lower()
    if lower_value not in valid_status:
        raise validationerror(f"Invalid status for {field_name}!. Enter one from ({'/'.join(valid_status)}).")
    return lower_value