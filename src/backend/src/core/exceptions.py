from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.exceptions import HTTPException as StarletteHTTPException


class ErrorResponseDTO(BaseModel):
    status_code: int
    detail: str
    path: str


def create_error_response(
    *,
    status_code: int,
    detail: str,
    path: str,
) -> JSONResponse:
    payload = ErrorResponseDTO(
        status_code=status_code,
        detail=detail,
        path=path,
    )
    return JSONResponse(status_code=status_code, content=payload.model_dump())


async def http_exception_handler(
    request: Request,
    exception: Exception,
) -> JSONResponse:
    if isinstance(exception, StarletteHTTPException):
        return create_error_response(
            status_code=exception.status_code,
            detail=str(exception.detail),
            path=request.url.path,
        )
    return create_error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Unexpected HTTP exception.",
        path=request.url.path,
    )


async def validation_exception_handler(
    request: Request,
    _exception: Exception,
) -> JSONResponse:
    return create_error_response(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        detail="Request validation failed.",
        path=request.url.path,
    )


async def unhandled_exception_handler(
    request: Request,
    _exception: Exception,
) -> JSONResponse:
    return create_error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Internal server error.",
        path=request.url.path,
    )


def register_exception_handlers(application: FastAPI) -> None:
    application.add_exception_handler(StarletteHTTPException, http_exception_handler)
    application.add_exception_handler(RequestValidationError, validation_exception_handler)
    application.add_exception_handler(Exception, unhandled_exception_handler)
