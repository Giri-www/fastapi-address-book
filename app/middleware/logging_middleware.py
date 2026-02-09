# app/middleware/logging_middleware.py



import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Generate unique request ID
        request_id = str(uuid.uuid4())

        # Attach request_id to request state
        request.state.request_id = request_id

        logger.info(
            f"Incoming request: {request.method} {request.url.path}",
            extra={"request_id": request_id},
        )

        try:
            response = await call_next(request)

            process_time = round(time.time() - start_time, 4)

            logger.info(
                f"Completed {response.status_code} in {process_time}s",
                extra={"request_id": request_id},
            )

            return response

        except Exception as e:
            logger.exception(
                f"Unhandled exception: {str(e)}",
                extra={"request_id": request_id},
            )
            raise

        finally:
            logger.info(
                f"Request completed: {request.method} {request.url.path}",
                extra={"request_id": request_id},
            )
