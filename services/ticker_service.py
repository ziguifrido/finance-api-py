import yfinance as yf

from services.service_exception import NotFoundException


class TickerService:
    def get_ticker_info(self, symbol: str):
        ticker = yf.Ticker(symbol)
        if not ticker or not ticker.info:
            raise NotFoundException(
                detail=f"Ticker ({symbol}) not found or no information available!"
            )
        return ticker.info
