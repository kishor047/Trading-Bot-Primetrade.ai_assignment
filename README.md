# Simplified Binance Futures Testnet Trading Bot

This project provides a small Python CLI for placing **MARKET** and **LIMIT** orders on the Binance **USDT-M Futures Testnet**. It includes validation, structured code separation, and logging of requests, responses, and errors.

## Setup

1. Create a Binance Futures Testnet account and generate API keys.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Export credentials:

```bash
export BINANCE_API_KEY="your_key"
export BINANCE_API_SECRET="your_secret"
```

## Usage

From the repository root:

```bash
python trading_bot/cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

```bash
python trading_bot/cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 65000
```

### Optional environment overrides

```bash
export BINANCE_TESTNET_BASE_URL="https://testnet.binancefuture.com"
export TRADING_BOT_LOG_FILE="logs/trading_bot.log"
```

## Output

The CLI prints:
- Order request summary
- Order response details (orderId, status, executedQty, avgPrice if available)
- Success or failure message

Logs are written to `logs/trading_bot.log` by default.

## Notes

- This CLI targets the **Binance Futures Testnet** only.
- Use **USDT-M** symbols (e.g., `BTCUSDT`).
