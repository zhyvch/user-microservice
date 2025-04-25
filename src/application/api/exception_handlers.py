import logging

from botocore.exceptions import UnknownKeyError
from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse
from pydantic import ValidationError
from sqlalchemy.exc import DatabaseError
from starlette.exceptions import HTTPException

from domain.exceptions.base import ApplicationException
from service.exceptions.base import ServiceException


logger = logging.getLogger(__name__)


def exception_registry(app: FastAPI) -> None:
    @app.exception_handler(ApplicationException)
    def handle_application_exception(request: Request, exc: ApplicationException):
        logger.error('%s: %s', exc.__class__.__name__, exc.message)
        return ORJSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                'message': f'{exc.message}',
            }
        )

    @app.exception_handler(ServiceException)
    def handle_application_exception(request: Request, exc: ServiceException):
        logger.critical('%s: %s', exc.__class__.__name__, exc.message)
        return ORJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                'message': f'{exc.message} \n we have already notified our team. Try again later.',
            }
        )

    @app.exception_handler(HTTPException)
    def handle_database_exception(request: Request, exc: HTTPException):
        logger.warning('%s: %r', exc.__class__.__name__, exc)
        return ORJSONResponse(
            status_code=exc.status_code,
            content={
                'message': f'{exc.detail}',
            }
        )

    @app.exception_handler(DatabaseError)
    def handle_database_exception(request: Request, exc: DatabaseError):
        logger.critical('%s: %r', exc.__class__.__name__, exc)
        return ORJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                'message': 'Database error occurred. We have already notified our team. Try again later.',
            }
        )

    @app.exception_handler(ValidationError)
    def handle_pydantic_validation_exception(request: Request, exc: ValidationError):
        logger.warning('%s: %s', exc.__class__.__name__, exc.errors())
        return ORJSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                'message': 'Exception during validation occurred',
            }
        )

    @app.exception_handler(UnknownKeyError)
    def handle_unknown_key_exception(request: Request, exc: UnknownKeyError):
        logger.warning('%s: %s', exc.__class__.__name__, exc)
        return ORJSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                'message': f'You likely haven\'t upload any image ({exc.fmt})',
            }
        )
