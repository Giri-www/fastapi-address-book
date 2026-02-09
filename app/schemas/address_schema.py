# app/schemas/address_schema.py
""" 
Schemas for Address API:

 Usage:
    1. Pydantic Validation
    2. Response Serialization
    3.  Data validation


"""

from pydantic import BaseModel, Field

class AddressBase(BaseModel):
    """ Base Schema for Address """
    name: str
    street: str
    city: str
    latitude: float = Field(..., ge=-90, le=90,description="Latitude must be between -90 and 90")
    longitude: float = Field(..., ge=-180, le=180,description="Longitude must be between -180 and 180")


class AddressCreate(AddressBase):
    """ Address Create Schema """
    pass


class AddressUpdate(AddressBase):
    """ Address Update Schema """
    pass


class AddressResponse(AddressBase):
    """ Address Response Schema Including ID """
    id: int

    model_config = {
        "from_attributes": True  
    }
