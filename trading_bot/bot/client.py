from __future__ import annotations

import hashlib
import hmac
import time
import urllib.parse
from typing import Any

import requests


class BinanceAPIError(Exception):
    def __init__(self, status_code: int, message: str, payload: Any | None = None) -> None:
        self.status_code = status_code
        self.payload = payload
        super().__init__(f"{status_code}: {message}")


class BinanceFuturesClient:
    def __init__(
        self,
        api_key: str,
        api_secret: str,
        base_url: str,
        timeout: int = 10,
        recv_window: int = 5000,
    ) -> None:
        if not api_key or not api_secret:
            raise ValueError("API key and secret are required.")

        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.recv_window = recv_window
        self._api_secret = api_secret.encode("utf-8")

        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": api_key})

    def create_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: str,
        price: str | None = None,
        time_in_force: str = "GTC",
    ) -> dict[str, Any]:
        params: dict[str, Any] = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }

        if order_type == "LIMIT":
            params["price"] = price
            params["timeInForce"] = time_in_force

        return self._signed_request("POST", "/fapi/v1/order", params)

    def _signed_request(self, method: str, path: str, params: dict[str, Any]) -> dict[str, Any]:
        params = dict(params)
        params["timestamp"] = int(time.time() * 1000)
        params.setdefault("recvWindow", self.recv_window)

        query_string = urllib.parse.urlencode(params, doseq=True)
        signature = hmac.new(
            self._api_secret,
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        signed_query = f"{query_string}&signature={signature}"
        url = f"{self.base_url}{path}"

        try:
            if method.upper() in {"GET", "DELETE"}:
                response = self.session.request(
                    method,
                    f"{url}?{signed_query}",
                    timeout=self.timeout,
                )
            else:
                response = self.session.request(
                    method,
                    url,
                    data=signed_query,
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                    timeout=self.timeout,
                )
        except requests.RequestException as exc:
            raise BinanceAPIError(0, f"Network error: {exc}") from exc

        return self._parse_response(response)

    @staticmethod
    def _parse_response(response: requests.Response) -> dict[str, Any]:
        try:
            payload = response.json()
        except ValueError as exc:
            raise BinanceAPIError(response.status_code, "Non-JSON response", response.text) from exc

        if response.status_code >= 400:
            message = payload.get("msg", payload)
            raise BinanceAPIError(response.status_code, str(message), payload)

        return payload
