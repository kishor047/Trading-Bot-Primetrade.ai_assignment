from __future__ import annotations

import argparse
import os
import sys
from typing import Any

from bot.client import BinanceAPIError, BinanceFuturesClient
from bot.logging_config import setup_logging
from bot.orders import place_order
from bot.validators import ValidationError, validate_order_inputs


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Binance Futures Testnet order CLI")
    parser.add_argument("--symbol", required=True, help="Trading symbol, e.g., BTCUSDT")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL"], help="Order side")
    parser.add_argument("--type", required=True, choices=["MARKET", "LIMIT"], dest="order_type")
    parser.add_argument("--quantity", required=True, help="Order quantity")
    parser.add_argument("--price", help="Limit price (required for LIMIT orders)")
    parser.add_argument("--api-key", help="Binance API key (or set BINANCE_API_KEY)")
    parser.add_argument("--api-secret", help="Binance API secret (or set BINANCE_API_SECRET)")
    parser.add_argument(
        "--base-url",
        default=os.getenv("BINANCE_TESTNET_BASE_URL", "https://testnet.binancefuture.com"),
        help="Binance Futures Testnet base URL",
    )
    return parser


def print_request_summary(request_payload: dict[str, Any]) -> None:
    print("Order request summary:")
    for key, value in request_payload.items():
        print(f"  {key}: {value}")


def print_response_summary(response_payload: dict[str, Any]) -> None:
    print("Order response details:")
    fields = ["orderId", "status", "executedQty", "avgPrice", "price"]
    for field in fields:
        if field in response_payload:
            print(f"  {field}: {response_payload[field]}")
    print("Full response:")
    print(response_payload)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    logger = setup_logging()

    api_key = args.api_key or os.getenv("BINANCE_API_KEY")
    api_secret = args.api_secret or os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        message = "Missing API credentials. Set BINANCE_API_KEY and BINANCE_API_SECRET."
        logger.error(message)
        print(f"Error: {message}")
        return 1

    try:
        order_inputs = validate_order_inputs(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
        )
    except ValidationError as exc:
        logger.error("Validation error: %s", exc)
        print(f"Error: {exc}")
        return 1

    try:
        client = BinanceFuturesClient(
            api_key=api_key,
            api_secret=api_secret,
            base_url=args.base_url,
        )
        request_payload, response_payload = place_order(client, order_inputs)
    except (BinanceAPIError, ValueError) as exc:
        logger.error("Order failed: %s", exc)
        print(f"Order failed: {exc}")
        return 1

    print_request_summary(request_payload)
    print_response_summary(response_payload)
    print("Order placed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
