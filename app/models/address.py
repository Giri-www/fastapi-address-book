# app/models/address.py
"""
Model for Address:

    - Define database table structure
    - Define column types and constraints
    - Act as ORM entity for CRUD operations
"""

from sqlalchemy import Column, Integer, String, Float
from  app.database.base import Base

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    street = Column(String, nullable=False)
    city = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    def __repr__(self):
        """
        String representation of .
        for debugging and logging.
        """
        return f"<Address(id={self.id}, name='{self.name}', city='{self.city}')>"