from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation


class ValidationError(ValueError):
    pass


@dataclass(frozen=True)
class OrderInputs:
    symbol: str
    side: str
    order_type: str
    quantity: str
    price: str | None


def normalize_symbol(symbol: str) -> str:
    value = symbol.strip().upper()
    if not value.isalnum():
        raise ValidationError("Symbol must be alphanumeric, e.g., BTCUSDT.")
    if len(value) < 6:
        raise ValidationError("Symbol looks too short for a USDT-M pair.")
    return value


def normalize_side(side: str) -> str:
    value = side.strip().upper()
    if value not in {"BUY", "SELL"}:
        raise ValidationError("Side must be BUY or SELL.")
    return value


def normalize_order_type(order_type: str) -> str:
    value = order_type.strip().upper()
    if value not in {"MARKET", "LIMIT"}:
        raise ValidationError("Order type must be MARKET or LIMIT.")
    return value


def parse_positive_decimal(raw: str, field_name: str) -> str:
    try:
        value = Decimal(str(raw))
    except InvalidOperation as exc:
        raise ValidationError(f"{field_name} must be a number.") from exc
    if value <= 0:
        raise ValidationError(f"{field_name} must be greater than 0.")
    return format(value, "f")


def validate_order_inputs(
    symbol: str,
    side: str,
    order_type: str,
    quantity: str,
    price: str | None,
) -> OrderInputs:
    normalized_symbol = normalize_symbol(symbol)
    normalized_side = normalize_side(side)
    normalized_order_type = normalize_order_type(order_type)
    normalized_quantity = parse_positive_decimal(quantity, "Quantity")

    normalized_price: str | None = None
    if normalized_order_type == "LIMIT":
        if price is None:
            raise ValidationError("Price is required for LIMIT orders.")
        normalized_price = parse_positive_decimal(price, "Price")
    elif price is not None:
        raise ValidationError("Price should not be provided for MARKET orders.")

    return OrderInputs(
        symbol=normalized_symbol,
        side=normalized_side,
        order_type=normalized_order_type,
        quantity=normalized_quantity,
        price=normalized_price,
    )
