import pytest
from bot.validators import (
    ValidationError,
    normalize_order_type,
    normalize_side,
    normalize_symbol,
    parse_positive_decimal,
    validate_order_inputs,
)


def test_normalize_symbol_valid():
    assert normalize_symbol("BTCUSDT") == "BTCUSDT"
    assert normalize_symbol("ethusdt") == "ETHUSDT"
    assert normalize_symbol("  BNBUSDT  ") == "BNBUSDT"


def test_normalize_symbol_invalid():
    with pytest.raises(ValidationError, match="must be alphanumeric"):
        normalize_symbol("BTC-USDT")
    with pytest.raises(ValidationError, match="too short"):
        normalize_symbol("BTC")


def test_normalize_side_valid():
    assert normalize_side("BUY") == "BUY"
    assert normalize_side("buy") == "BUY"
    assert normalize_side("  SELL  ") == "SELL"


def test_normalize_side_invalid():
    with pytest.raises(ValidationError, match="must be BUY or SELL"):
        normalize_side("HOLD")


def test_normalize_order_type_valid():
    assert normalize_order_type("MARKET") == "MARKET"
    assert normalize_order_type("limit") == "LIMIT"


def test_normalize_order_type_invalid():
    with pytest.raises(ValidationError, match="must be MARKET or LIMIT"):
        normalize_order_type("STOP")


def test_parse_positive_decimal_valid():
    assert parse_positive_decimal("1.5", "Test") == "1.5"
    assert parse_positive_decimal("0.001", "Test") == "0.001"
    assert parse_positive_decimal("100", "Test") == "100"


def test_parse_positive_decimal_invalid():
    with pytest.raises(ValidationError, match="must be a number"):
        parse_positive_decimal("invalid", "Test")
    with pytest.raises(ValidationError, match="must be greater than 0"):
        parse_positive_decimal("0", "Test")
    with pytest.raises(ValidationError, match="must be greater than 0"):
        parse_positive_decimal("-1", "Test")


def test_validate_order_inputs_market_order():
    inputs = validate_order_inputs(
        symbol="BTCUSDT",
        side="BUY",
        order_type="MARKET",
        quantity="0.001",
        price=None,
    )
    assert inputs.symbol == "BTCUSDT"
    assert inputs.side == "BUY"
    assert inputs.order_type == "MARKET"
    assert inputs.quantity == "0.001"
    assert inputs.price is None


def test_validate_order_inputs_limit_order():
    inputs = validate_order_inputs(
        symbol="ETHUSDT",
        side="SELL",
        order_type="LIMIT",
        quantity="1.5",
        price="2500",
    )
    assert inputs.symbol == "ETHUSDT"
    assert inputs.side == "SELL"
    assert inputs.order_type == "LIMIT"
    assert inputs.quantity == "1.5"
    assert inputs.price == "2500"


def test_validate_order_inputs_limit_missing_price():
    with pytest.raises(ValidationError, match="Price is required"):
        validate_order_inputs(
            symbol="BTCUSDT",
            side="BUY",
            order_type="LIMIT",
            quantity="0.001",
            price=None,
        )


def test_validate_order_inputs_market_with_price():
    with pytest.raises(ValidationError, match="Price should not be provided for MARKET"):
        validate_order_inputs(
            symbol="BTCUSDT",
            side="BUY",
            order_type="MARKET",
            quantity="0.001",
            price="50000",
        )
