from http.client import HTTPException
from services.service_exception import NotFoundException
import yfinance as yf

class TickerService:
    def get_ticker_info(self, symbol: str):
        ticker = yf.Ticker(symbol)
        if not ticker or not ticker.info or ticker.info.get('trailingPegRatio') == None:
            raise NotFoundException(detail=f'Ticker ({symbol}) not found or no information available.')
        return ticker.info
        