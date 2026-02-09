# app/core/exceptions.py

"""
Custom Application Exceptions
------------------------------

This module defines custom exceptions used across
the application to maintain consistent error handling.

Responsibilities:
- Provide structured exception format
- Standardize error codes and messages
- Separate business errors from system errors
"""

class AppException(Exception):
    
    """ 
    Base class for custom application exceptions.
    
    All custom exceptions should inherit from this class.
    
    Args:
        message (str): Human-readable error message
        code (str): Unique error code
        status_code (int): HTTP status code
    """
    def __init__(self, message: str, code: str, status_code: int = 400):
        self.message = message
        self.code = code
        self.status_code = status_code


class NotFoundException(AppException):
    
    """
    Exception for resource not found errors.
    
    Args:
        message (str): service-layer handled error message
    """
    def __init__(self, message="Resource not found"):
        super().__init__(message, "NOT_FOUND", 404)
