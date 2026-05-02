from fastapi import APIRouter, Request, status

from services.rate_limit import limiter
from services.ticker_service import TickerService

router = APIRouter(prefix="/ticker")
service = TickerService()


@router.get("/{symbol}", status_code=status.HTTP_200_OK)
@limiter.limit("30/minute")
def get_ticker_info(request: Request, symbol: str):
    return service.get_ticker_info(symbol)
