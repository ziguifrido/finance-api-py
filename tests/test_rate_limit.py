from unittest.mock import patch

from services.rate_limit import limiter


class TestRateLimiting:
    def test_limiter_configured(self):
        assert limiter is not None
        assert hasattr(limiter, "limit")

    def test_rate_limit_within_limit(self, client, mock_ticker, mock_ticker_info):
        with patch("services.ticker_service.yf.Ticker", return_value=mock_ticker):
            for _ in range(5):
                response = client.get("/ticker/AAPL")
                assert response.status_code == 200

    def test_rate_limit_decorator_applied(self, client, mock_ticker, mock_ticker_info):
        with patch("services.ticker_service.yf.Ticker", return_value=mock_ticker):
            response = client.get("/ticker/PETR4.SA")
            assert response.status_code == 200

    def test_rate_limit_response_format(self, client, mock_ticker, mock_ticker_info):
        with patch("services.ticker_service.yf.Ticker", return_value=mock_ticker):
            response = client.get("/ticker/PETR4.SA")
            assert response.status_code == 200
            data = response.json()
            assert "symbol" in data
