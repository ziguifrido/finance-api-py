from unittest.mock import MagicMock, patch

import pytest

from services.service_exception import (
    InvalidInputException,
    NotFoundException,
    ServiceUnavailableException,
)
from services.ticker_service import TickerService


class TestTickerService:
    def test_get_ticker_info_success(self, mock_ticker, mock_ticker_info):
        with patch("services.ticker_service.yf.Ticker", return_value=mock_ticker):
            service = TickerService()
            result = service.get_ticker_info("PETR4.SA")
            assert result == mock_ticker_info

    def test_get_ticker_info_not_found(self):
        mock_ticker = MagicMock()
        mock_ticker.info = None

        with patch("services.ticker_service.yf.Ticker", return_value=mock_ticker):
            service = TickerService()
            with pytest.raises(NotFoundException) as exc_info:
                service.get_ticker_info("INVALID.SA")
            assert "INVALID.SA" in str(exc_info.value.detail)
            assert exc_info.value.status_code == 404

    def test_get_ticker_info_empty_ticker(self):
        with patch("services.ticker_service.yf.Ticker", return_value=None):
            service = TickerService()
            with pytest.raises(NotFoundException):
                service.get_ticker_info("NOTFOUND")

    def test_get_ticker_info_brazilian_ticker(self, mock_ticker, mock_ticker_info):
        with patch("services.ticker_service.yf.Ticker", return_value=mock_ticker):
            service = TickerService()
            result = service.get_ticker_info("MXRF11.SA")
            assert result["symbol"] == "PETR4.SA"

    def test_get_ticker_info_international_ticker(self, mock_ticker, mock_ticker_info):
        with patch("services.ticker_service.yf.Ticker", return_value=mock_ticker):
            service = TickerService()
            result = service.get_ticker_info("AAPL")
            assert result["symbol"] == "PETR4.SA"

    def test_get_ticker_info_invalid_symbol(self):
        service = TickerService()
        with pytest.raises(InvalidInputException) as exc_info:
            service.get_ticker_info("AAPL$")
        assert exc_info.value.status_code == 400

    def test_get_ticker_info_upstream_error(self):
        with patch(
            "services.ticker_service.yf.Ticker", side_effect=RuntimeError("timeout")
        ):
            service = TickerService()
            with pytest.raises(ServiceUnavailableException) as exc_info:
                service.get_ticker_info("AAPL")
            assert exc_info.value.status_code == 503
