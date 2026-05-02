from fastapi import FastAPI
from fastapi import Request as FastAPIRequest
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from starlette.responses import Response

from controllers.ticker_controller import router as ticker_router
from services.rate_limit import limiter
from services.service_exception import ServiceException


async def rate_limit_exceeded_handler(
    request: FastAPIRequest, exc: Exception
) -> Response:
    return JSONResponse(
        status_code=429,
        content={
            "message": "Rate limit exceeded",
            "code": 429,
        },
    )


app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

app.include_router(ticker_router)


@app.exception_handler(ServiceException)
async def service_exception_handler(request: FastAPIRequest, exc: ServiceException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.detail,
            "code": exc.error_code,
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
