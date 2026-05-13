from unittest.mock import MagicMock, patch


class TestMainApp:
    def test_service_exception_handler_not_found(self, client):
        mock_ticker = MagicMock()
        mock_ticker.info = None

        with patch("services.ticker_service.yf.Ticker", return_value=mock_ticker):
            response = client.get("/ticker/NOTFOUND")
            assert response.status_code == 404
            data = response.json()
            assert "message" in data
            assert "code" in data
            assert data["code"] == "NOT_FOUND"

    def test_app_includes_ticker_router(self, client):
        with patch("services.ticker_service.yf.Ticker") as mock_ticker_class:
            mock_ticker = mock_ticker_class.return_value
            mock_ticker.info = {"symbol": "AAPL", "shortName": "Apple"}
            response = client.get("/ticker/AAPL")
            assert response.status_code == 200
            assert response.json()["symbol"] == "AAPL"

    def test_exception_response_format(self, client):
        mock_ticker = MagicMock()
        mock_ticker.info = None

        with patch("services.ticker_service.yf.Ticker", return_value=mock_ticker):
            response = client.get("/ticker/UNKNOWN")
            assert response.status_code == 404
            data = response.json()
            assert "message" in data
            assert "code" in data
            assert data["code"] == "NOT_FOUND"
