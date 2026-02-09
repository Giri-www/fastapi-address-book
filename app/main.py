from fastapi import FastAPI
from app.core.config import APP_NAME, API_VERSION
from app.core.exception_handelers import app_exception_handler
from app.core.exceptions import AppException
from app.database.base import Base
from app.database.session import engine
from app.api.address_api import router
from app.middleware.logging_middleware import LoggingMiddleware
from fastapi.exceptions import RequestValidationError
from app.core.exception_handelers import validation_exception_handler,app_exception_handler

Base.metadata.create_all(bind=engine)

app = FastAPI(title=APP_NAME, version=API_VERSION)

app.add_exception_handler(AppException, app_exception_handler)

# Validation error handler
app.add_exception_handler(RequestValidationError, validation_exception_handler)


app.include_router(router)
app.add_middleware(LoggingMiddleware)
