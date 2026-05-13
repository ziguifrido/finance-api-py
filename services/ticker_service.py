import re
from typing import Any

import yfinance as yf

from services.service_exception import (
    InvalidInputException,
    NotFoundException,
    ServiceUnavailableException,
)


class TickerService:
    _symbol_pattern = re.compile(r"^[A-Za-z0-9.-]{1,16}$")

    def get_ticker_info(self, symbol: str) -> dict[str, Any]:
        normalized_symbol = symbol.strip().upper()
        if not self._symbol_pattern.fullmatch(normalized_symbol):
            raise InvalidInputException(
                detail=(
                    "Invalid ticker symbol format. Use up to 16 characters from "
                    "letters, numbers, dot, and hyphen."
                )
            )

        try:
            ticker = yf.Ticker(normalized_symbol)
            ticker_info = ticker.info if ticker else None
        except Exception as exc:
            raise ServiceUnavailableException(
                detail="Unable to fetch ticker data from upstream provider."
            ) from exc

        if not ticker_info:
            raise NotFoundException(
                detail=(
                    f"Ticker ({normalized_symbol}) not found or no information "
                    "available!"
                )
            )
        if not isinstance(ticker_info, dict):
            raise ServiceUnavailableException(
                detail="Unexpected ticker payload received from upstream provider."
            )
        return ticker_info
