# 🚀 Binance Futures Testnet Trading Bot (Python CLI)

A lightweight Python-based CLI trading bot for executing **MARKET** and **LIMIT** orders on the **Binance USDT-M Futures Testnet**.  
This project demonstrates API integration, modular architecture, and automated trading execution using Python.

---

## 📌 Features

- ✅ Place MARKET and LIMIT orders
- ✅ Binance USDT-M Futures Testnet support
- ✅ Clean CLI interface
- ✅ Modular project structure (client, CLI, logging)
- ✅ Request & response logging
- ✅ Environment-based API key management

---

## 🧰 Tech Stack

- Python 3.9+
- Binance Futures API
- Requests library
- CLI-based execution

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/binance-trading-bot.git
cd binance-trading-bot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Configuration

Create a `.env` file in the root folder:

```env
BINANCE_API_KEY=your_api_key
BINANCE_API_SECRET=your_api_secret
```

**OR** set environment variables manually:

**Windows (PowerShell)**

```powershell
setx BINANCE_API_KEY "your_api_key"
setx BINANCE_API_SECRET "your_api_secret"
```

**Linux / macOS**

```bash
export BINANCE_API_KEY="your_api_key"
export BINANCE_API_SECRET="your_api_secret"
```

---

## ▶️ Usage

Run the bot from the project root:

**📈 MARKET ORDER**

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

**📉 LIMIT ORDER**

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 65000
```

---

## 📊 Output

The CLI will display:

- Order request summary
- API response (`orderId`, `status`, executed quantity, price)
- Success or error messages

Logs are saved in:

```
logs/trading_bot.log
```

---

## 🚀 Future Improvements

- Trading strategies (EMA / RSI / MACD)
- Stop-loss & take-profit system
- Backtesting engine
- Live dashboard (Flask / FastAPI)
- Docker deployment
- Risk management system
