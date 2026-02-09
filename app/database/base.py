# app/database/base.py

"""
Database Base Configuration
##########################

This module defines the SQLAlchemy Declarative Base.

The Base class is used as the parent class for all
ORM models in the application.

Responsibilities:
- Acts as a registry for all database models
- Allows SQLAlchemy to map Python classes to DB tables
- Used by migrations and metadata creation

"""

from sqlalchemy.orm import declarative_base

Base = declarative_base()
