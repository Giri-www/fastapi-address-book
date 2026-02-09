# app/api/address_api.py

""" Address API  For  Handeling HTTP Endpoints """

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.address_service import AddressService
from app.schemas.address_schema import AddressCreate, AddressUpdate
from app.core.responses import SuccessResponse
from app.core.responses import PaginatedSuccessResponse, AddressResponse, PaginatedMeta
from math import ceil
from fastapi import Query

router = APIRouter(prefix="/addresses", tags=["Addresses"])


@router.post("/")
def create_address(data: AddressCreate, db: Session = Depends(get_db)):
    """
    Create a new address.

    Args:
        data (AddressCreate): Address data payload
        db (Session): SQLAlchemy database session

    Returns:
        SuccessResponse: Standardized success response with created address
    
    """
    result = AddressService.create(db, data)
    return SuccessResponse(data=result, message="Created successfully").dict()


@router.put("/{address_id}",)
def update_address(address_id: int,
                   data: AddressUpdate,
                   db: Session = Depends(get_db)):
    """ Update an existing address by its ID.

    Args:
        address_id (int): ID of the address to update
        data (AddressUpdate): Updated address data
        db (Session): SQLAlchemy database session

    Returns:
        SuccessResponse: Standardized success response with updated address
    """

    result = AddressService.update(db, address_id, data)

    return SuccessResponse(
        message="Address updated successfully",
        data=result
    )

@router.get("/list/", response_model=PaginatedSuccessResponse)
def list_addresses(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    search: str = Query(None, description="Search by name or city"),
    sort_by: str = Query("id", description="Sort by field"),
    sort_order: str = Query("asc", regex="^(asc|desc)$", description="Sort order")
):
    """
    Retrieve a paginated list of addresses with optional search and sorting.

    Args:
        db (Session): SQLAlchemy database session
        page (int): Current page number
        page_size (int): Number of items per page
        search (str, optional): Search term to filter addresses by name or city
        sort_by (str): Field name to sort by
        sort_order (str): Sorting order: 'asc' or 'desc'

    Returns:
        PaginatedSuccessResponse: Standardized response with pagination metadata and list of addresses
    """
    
    skip = (page - 1) * page_size

    # Fetch paginated + filtered + sorted addresses from service
    results, total = AddressService.get_all(db,skip=skip,limit=page_size,search=search,sort_by=sort_by,sort_order=sort_order)

    total_pages = ceil(total / page_size) if total else 1

    return PaginatedSuccessResponse(
        message="Addresses fetched successfully",
        meta=PaginatedMeta(
            page=page,
            page_size=page_size,
            total=total,
            total_pages=total_pages
        ),
        data=[AddressResponse.from_orm(a) for a in results]
    )

@router.delete("/{address_id}")
def delete_address(address_id: int, db: Session = Depends(get_db)):
    
    """
    Delete an address by its ID.

    Args:
        address_id (int): ID of the address to delete
        db (Session): SQLAlchemy database session

    Returns:
        SuccessResponse: Standardized success response confirming deletion
    """
    AddressService.delete(db, address_id)
    return SuccessResponse(message="Deleted successfully").dict()

@router.get("/nearby/", response_model=PaginatedSuccessResponse)
def nearby_addresses(
    lat: float = Query(..., description="Latitude of the center point"),
    lon: float = Query(..., description="Longitude of the center point"),
    distance: float = Query(..., description="Radius in kilometers to search"),
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),
):
    """
    Retrieve nearby addresses within a given distance from coordinates
    with pagination.
    """
    skip = (page - 1) * page_size

    # Fetch all nearby addresses from service
    results, total = AddressService.nearby(
        db,
        lat=lat,
        lon=lon,
        distance=distance,
        skip=skip,
        limit=page_size
    )

    total_pages = ceil(total / page_size) if total else 1
    
    if not results:
        return PaginatedSuccessResponse(
            message="No nearby addresses found",
            meta=PaginatedMeta(
                page=page,
                page_size=page_size,
                total=total,
                total_pages=total_pages
            ),
            data=[]
        )

    return PaginatedSuccessResponse(
        message="Nearby addresses fetched successfully",
        meta=PaginatedMeta(
            page=page,
            page_size=page_size,
            total=total,
            total_pages=total_pages
        ),
        data=[AddressResponse.from_orm(a) for a in results]
    )
