from fastapi import APIRouter, status
from services.ticker_service import TickerService

router = APIRouter(prefix='/ticker')
service = TickerService()

@router.get('/{symbol}', status_code=status.HTTP_200_OK)
def get_ticker_info(symbol: str):
    return service.get_ticker_info(symbol)
