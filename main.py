from urllib.request import Request
from fastapi import FastAPI
from controllers.ticker_controller import router as ticker_router
from services.service_exception import ServiceException
from fastapi.responses import JSONResponse


app = FastAPI()

app.include_router(ticker_router)

@app.exception_handler(ServiceException)
async def service_exception_handler(request: Request, exc: ServiceException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.detail,
            "code": exc.error_code,
        },
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9999)