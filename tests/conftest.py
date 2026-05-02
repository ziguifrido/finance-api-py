from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_ticker_info():
    return {
        "symbol": "PETR4.SA",
        "shortName": "Petrobras",
        "longName": "Petroleo Brasileiro S.A.",
        "regularMarketPrice": 38.5,
        "sector": "Energy",
        "industry": "Oil & Gas Integrated",
    }


@pytest.fixture
def mock_ticker(mock_ticker_info):
    mock = MagicMock()
    mock.info = mock_ticker_info
    return mock
