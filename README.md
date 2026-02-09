# Address API

## Overview

**Address API** is a FastAPI-based backend service for managing addresses.  
It is designed following **industry-standard architecture** with layered design, standardized responses, and scalable endpoints.

The API provides:

- CRUD operations for addresses
- Paginated listing with search and sorting
- Nearby address search using latitude, longitude, and distance
- Standardized JSON responses
- Custom exception handling

---

## Architecture & Approach

### Layered Architecture

This project follows **API → Service → Repository → Database** separation:

API Layer --> FastAPI routes handling HTTP requests and responses
Service Layer --> Business logic, pagination, search, sorting, and distance calculation
Repo Layer--> Direct database operations (CRUD)
Database --> SQLAlchemy models, PostgreSQL or any supported DB
Utils --> Utility functions like haversine for distance
Schemas --> For Pydantic Validation
core --> 