# app/repo/address_repo.py

""" 
DB Access Layer for Address API 

    - Executes database queries
    - Manages DB Operations
    - Performs CRUD operations

"""

from sqlalchemy.orm import Session
from app.models.address import Address


class AddressRepository:

    @staticmethod
    def create(db: Session, address: Address):
        """
        Create a new address record.

        Args:
            db (Session): Active database session
            address (Address): Address ORM object

        Returns:
            Address: Newly created address object
        """
        db.add(address)
        db.commit()
        db.refresh(address)
        return address

    @staticmethod
    def get(db: Session, address_id: int, skip: int = 0, limit: int = 100):
        """
        Fetch a single address by ID.

        Args:
            db (Session): Active database session
            address_id (int): Address primary key

        Returns:
            Address | None:
                Address object if found,
                otherwise None.
        """
        return db.query(Address).filter(Address.id == address_id).first()

    @staticmethod
    def get_all(db: Session):
        """
        Fetch all address records from database.

        Args:
            db (Session): Active database session

        Returns:
            List[Address]: List of all addresses
        """
        return db.query(Address).all()
    
    @staticmethod
    def update(db: Session, address: Address,update_data: dict = None):
        """
        Update an existing address record.

        Args:
            db (Session): Active database session
            address (Address): Address ORM object to update

        Returns:
            Address: Updated address object
        """
        for key, value in update_data.items():
            setattr(address, key, value)
        db.commit()
        db.refresh(address)
        return address

    @staticmethod
    def delete(db: Session, address: Address):
        """
        Delete an existing address record.

        Args:
            db (Session): Active database session
            address (Address): Address ORM object to delete
        """
        db.delete(address)
        db.commit()
