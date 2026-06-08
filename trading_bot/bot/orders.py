from __future__ import annotations

from typing import Any

from .client import BinanceFuturesClient
from .logging_config import setup_logging
from .validators import OrderInputs

logger = setup_logging()


def place_order(client: BinanceFuturesClient, order: OrderInputs) -> tuple[dict[str, Any], dict[str, Any]]:
    request_payload: dict[str, Any] = {
        "symbol": order.symbol,
        "side": order.side,
        "type": order.order_type,
        "quantity": order.quantity,
    }

    if order.order_type == "LIMIT":
        request_payload["price"] = order.price
        request_payload["timeInForce"] = "GTC"

    logger.info("Order request: %s", request_payload)
    response = client.create_order(
        symbol=order.symbol,
        side=order.side,
        order_type=order.order_type,
        quantity=order.quantity,
        price=order.price,
    )
    logger.info("Order response: %s", response)

    return request_payload, response
