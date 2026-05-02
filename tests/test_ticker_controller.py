from unittest.mock import MagicMock, patch


class TestTickerController:
    def test_get_ticker_info_success(self, client, mock_ticker, mock_ticker_info):
        with patch("services.ticker_service.yf.Ticker", return_value=mock_ticker):
            response = client.get("/ticker/PETR4.SA")
            assert response.status_code == 200
            assert response.json()["symbol"] == "PETR4.SA"
            assert response.json()["shortName"] == "Petrobras"

    def test_get_ticker_info_not_found(self, client):
        mock_ticker = MagicMock()
        mock_ticker.info = None

        with patch("services.ticker_service.yf.Ticker", return_value=mock_ticker):
            response = client.get("/ticker/INVALID.SA")
            assert response.status_code == 404
            assert "INVALID.SA" in response.json()["message"]

    def test_get_ticker_info_brazilian_reit(
        self, client, mock_ticker, mock_ticker_info
    ):
        with patch("services.ticker_service.yf.Ticker", return_value=mock_ticker):
            response = client.get("/ticker/MXRF11.SA")
            assert response.status_code == 200

    def test_get_ticker_info_international_stock(
        self, client, mock_ticker, mock_ticker_info
    ):
        with patch("services.ticker_service.yf.Ticker", return_value=mock_ticker):
            response = client.get("/ticker/AAPL")
            assert response.status_code == 200
