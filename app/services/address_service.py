# app/services/address_service.py

"""
Business Logic Layer for Address API
####################################

This module contains all the core business logic for managing addresses.
Responsibilities include:
- Creating, updating, deleting addresses
- Fetching all addresses with pagination, search, and sorting
- Retrieving nearby addresses using distance calculations
- Handling exceptions for not found resources

It acts as a bridge between the repository layer and API layer,
keeping the service logic centralized and reusable.
"""

from app.repo.address_repo import AddressRepository
from app.core.exceptions import NotFoundException
from app.models.address import Address
from app.utils.distance import haversine
from app.core.logger import logger
from sqlalchemy.orm import Session
class AddressService:

    @staticmethod
    def create(db, data):
        """
        Create a new address record.

        Args:
            db (Session): SQLAlchemy database session
            data (AddressCreate): Pydantic model with address fields

        Returns:
            Address: Created address object
        """
        address = Address(**data.dict())
        return AddressRepository.create(db, address)
    
    @staticmethod
    def update(db, address_id, data):
        """
        Update an existing address by ID.

        Args:
            db (Session): SQLAlchemy database session
            address_id (int): ID of the address to update
            data (AddressUpdate): Pydantic model with updated fields

        Raises:
            NotFoundException: If address with given ID does not exist

        Returns:
            Address: Updated address object
        """
        address = AddressRepository.get(db, address_id)
        if not address:
            raise NotFoundException("Address not found")
        
        update_data = data.dict(exclude_unset=True)
        
        return AddressRepository.update(db, address, data.dict())

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 10, search: str = None, sort_by: str = "id", sort_order: str = "asc"):
        """
        Retrieve addresses with optional search, sorting, and pagination.

        Args:
            db (Session): SQLAlchemy database session
            skip (int): Number of records to skip (pagination)
            limit (int): Maximum number of records to return
            search (str, optional): Filter addresses by name or city
            sort_by (str): Column name to sort by
            sort_order (str): 'asc' or 'desc' for sorting order

        Returns:
            Tuple[List[Address], int]: List of addresses and total count
        """
        query = db.query(Address)

        # search filter
        if search:
            query = query.filter(
                (Address.name.ilike(f"%{search}%")) |
                (Address.city.ilike(f"%{search}%"))
            )

        # sorting
        sort_column = getattr(Address, sort_by, Address.id)
        sort_column = sort_column.desc() if sort_order == "desc" else sort_column.asc()
        query = query.order_by(sort_column)

        total = query.count()
        results = query.offset(skip).limit(limit).all()
        return results, total

    @staticmethod
    def delete(db, address_id):
        """
        Delete an address by ID.

        Args:
            db (Session): SQLAlchemy database session
            address_id (int): ID of the address to delete

        Raises:
            NotFoundException: If address with given ID does not exist
        """
        address = AddressRepository.get(db, address_id)
        if not address:
            raise NotFoundException("Address not found")

        AddressRepository.delete(db, address)

    @staticmethod
    def nearby(db, lat, lon, distance, skip=0, limit=10):
        """
        Retrieve addresses within a certain distance from given coordinates
        using the Python haversine function, with pagination support.

        Args:
            db (Session): SQLAlchemy database session
            lat (float): Latitude of the center point
            lon (float): Longitude of the center point
            distance (float): Radius in kilometers to search within
            skip (int): Number of records to skip (pagination)
            limit (int): Maximum number of records to return

        Returns:
            Tuple[List[Address], int]: Paginated list of nearby addresses and total count
        """

        # Fetch all addresses 
        addresses = AddressRepository.get_all(db)

        # Filter haversine
        nearby_addresses = [
            addr for addr in addresses
            if haversine(lat, lon, addr.latitude, addr.longitude) <= distance
        ]

        total = len(nearby_addresses)

        # pagination
        paginated_results = nearby_addresses[skip: skip + limit]

        return paginated_results, total