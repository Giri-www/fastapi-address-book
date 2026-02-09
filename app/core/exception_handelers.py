# app/core/exception_handelers.py

"""
Global Exception Handlers
##########################

This module contains custom exception handlers used across
the application.

Responsibilities:
- Catch application-specific exceptions
- Return standardized error responses
- Maintain consistent API error format

helps :  frontend and API consumers handle errors reliably.
"""
# app/core/exception_handlers.py

from fastapi.responses import JSONResponse
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from .exceptions import AppException


async def app_exception_handler(request: Request, exc: AppException):
    """
    Handles custom application exceptions.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.code,
                "message": exc.message
            }
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handles Pydantic validation errors.
    """
    fields = []

    for err in exc.errors():
        field_name = ".".join(str(loc) for loc in err.get("loc", []) if loc != "body")
        error_type = _normalize_error_type(err.get("type"))
        input_value = err.get("ctx", {}).get("given") if "given" in err.get("ctx", {}) else err.get("input")
        constraints = {k: v for k, v in (err.get("ctx") or {}).items() if k != "given"}

        fields.append({
            "name": field_name,
            "error_type": error_type,
            "message": err.get("msg"),
            "input": input_value,
            "constraints": constraints
        })

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Validation failed for one or more fields.",
                "fields": fields
            }
        }
    )


def _normalize_error_type(error_type: str) -> str:
    """
    Converts Pydantic error types to readable codes.
    """
    mapping = {
        "value_error.missing": "required",
        "type_error.integer": "type_error_integer",
        "type_error.float": "type_error_float",
        "value_error.number.not_ge": "greater_than_equal",
        "value_error.number.not_le": "less_than_equal",
        "value_error.any_str.min_length": "min_length",
        "value_error.any_str.max_length": "max_length",
    }
    return mapping.get(error_type, error_type)
