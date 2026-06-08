from unittest.mock import MagicMock, patch

import pytest
import requests

from bot.client import BinanceAPIError, BinanceFuturesClient


def test_binance_futures_client_init():
    client = BinanceFuturesClient(
        api_key="test_key",
        api_secret="test_secret",
        base_url="https://testnet.binancefuture.com",
    )
    assert client.base_url == "https://testnet.binancefuture.com"
    assert client.timeout == 10
    assert client.recv_window == 5000


def test_binance_futures_client_init_missing_credentials():
    with pytest.raises(ValueError, match="API key and secret are required"):
        BinanceFuturesClient(api_key="", api_secret="secret", base_url="https://test.com")
    with pytest.raises(ValueError, match="API key and secret are required"):
        BinanceFuturesClient(api_key="key", api_secret="", base_url="https://test.com")


@patch("bot.client.requests.Session.request")
def test_create_order_market(mock_request):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"orderId": "12345", "status": "FILLED"}
    mock_request.return_value = mock_response

    client = BinanceFuturesClient(
        api_key="test_key",
        api_secret="test_secret",
        base_url="https://testnet.binancefuture.com",
    )
    result = client.create_order(
        symbol="BTCUSDT",
        side="BUY",
        order_type="MARKET",
        quantity="0.001",
    )
    assert result["orderId"] == "12345"
    assert result["status"] == "FILLED"


@patch("bot.client.requests.Session.request")
def test_create_order_limit(mock_request):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"orderId": "12346", "status": "NEW"}
    mock_request.return_value = mock_response

    client = BinanceFuturesClient(
        api_key="test_key",
        api_secret="test_secret",
        base_url="https://testnet.binancefuture.com",
    )
    result = client.create_order(
        symbol="ETHUSDT",
        side="SELL",
        order_type="LIMIT",
        quantity="1.5",
        price="2500",
    )
    assert result["orderId"] == "12346"
    assert result["status"] == "NEW"


@patch("bot.client.requests.Session.request")
def test_api_error_response(mock_request):
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.json.return_value = {"msg": "Invalid symbol"}
    mock_request.return_value = mock_response

    client = BinanceFuturesClient(
        api_key="test_key",
        api_secret="test_secret",
        base_url="https://testnet.binancefuture.com",
    )
    with pytest.raises(BinanceAPIError, match="400"):
        client.create_order(
            symbol="INVALID",
            side="BUY",
            order_type="MARKET",
            quantity="0.001",
        )


@patch("bot.client.requests.Session.request")
def test_network_error(mock_request):
    mock_request.side_effect = requests.RequestException("Network error")

    client = BinanceFuturesClient(
        api_key="test_key",
        api_secret="test_secret",
        base_url="https://testnet.binancefuture.com",
    )
    with pytest.raises(BinanceAPIError, match="Network error"):
        client.create_order(
            symbol="BTCUSDT",
            side="BUY",
            order_type="MARKET",
            quantity="0.001",
        )
