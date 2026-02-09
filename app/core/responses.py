# app/core/responses.py

"""  
Custom Response Class For API Endpoints 

1. SuccessResponse for Standardized Success Response
2. PaginatedSuccessResponse for Standardized Paginated Response

    - Maintains Consistent API Response Format
    - Standardizes Success and Error Responses
    - Separates Business and System Errors
    - Helps Frontend and API Consumers Handle Errors Reliably
    

"""

from typing import Any, Optional
from pydantic import BaseModel
from app.schemas.address_schema import AddressResponse

class SuccessResponse:
    def __init__(
        self,
        data: Any = None,
        message: str = "Success",
        meta: Optional[dict] = None
    ):
        self.success = True
        self.message = message
        self.data = data
        self.meta = meta or {}

    def dict(self):
        return {
            "success": self.success,
            "message": self.message,
            "data": self.data,
            "meta": self.meta
        }


# Pagination metadata
class PaginatedMeta(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int


# Paginated response
class PaginatedSuccessResponse(BaseModel):
    success: bool = True
    message: str = "Fetched successfully"
    meta: PaginatedMeta
    data: list[AddressResponse]
    
    model_config = {
        "from_attributes": True  
    }