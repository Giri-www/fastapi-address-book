# Fast Address API CRUD 


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

- **API Layer** → FastAPI routes handling HTTP requests and responses.  
- **Core** → Exception handlers, custom exceptions, universal response models, configuration files.  
- **Database** → SQLAlchemy models, supports SQLite (default) or PostgreSQL.  
- **Service Layer** → Business logic, pagination, search, sorting, and distance calculation.  
- **Repository Layer** → Direct database operations (CRUD).  
- **Utils** → Utility functions, e.g., haversine distance calculation.  
- **Schemas** → Pydantic models for request validation and response serialization.  
- **Middleware** → Logger middleware for API debugging and monitoring console output.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/giri-www/fastapi-address-book.git
cd fastapi-address-book

```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
  
```
3. Install dependencies:

pip install -r .\requirements\dev.txt    

```


4. Database Setup (using SQLAlchemy default SQLite):

```
5.Run the application:

```bash
uvicorn app.main:app --reload

```
6. Open Swagger UI to test endpoints:

```bash
http://127.0.0.1:8000/docs

```