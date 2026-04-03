
# 🤖 Binance Futures Trading Bot (Testnet)

A robust, production-grade Python CLI bot designed for algorithmic trading on the **Binance Futures Testnet**. 

This project demonstrates industry-standard practices including **dynamic input validation**, **asynchronous polling** for accurate order fills, and **comprehensive error handling**.

---

## ✨ Highlights

*   🚀 **Instant Execution:** Places Market and Limit orders with millisecond precision.
*   🛡️ **Smart Validation:** Automatically fetches exchange rules (Lot Size) to ensure your order quantity is accepted by Binance.
*   📊 **Real-Time Feedback:** Polls the exchange to return the *actual* average price and filled quantity (not just the initial request).
*   📝 **Detailed Logging:** Every API request and response is timestamped and saved to `logs/trading_bot.log`.
*   🎨 **Modern CLI:** Built with `Typer` for a clean, user-friendly command-line interface.

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

1.  **Python 3.8+** ([Download here](https://www.python.org/downloads/))
2.  **PIP** (Usually comes with Python).
3.  **Binance Futures Testnet Account**:
    *   Sign up here: [https://testnet.binancefuture.com](https://testnet.binancefuture.com)
    *   Generate API Keys with **"Enable Futures"** permission checked.

---

## 🚀 Quick Start Guide

Get up and running in 4 simple steps.

### 1. Clone the Repository
```bash
git clone https://github.com/Prathameshsci369/Binance-Futures-Trading-Bot-Testnet-.git
cd binance-futures-trading-bot
```

### 2. Create Virtual Environment (Recommended)
This keeps your project dependencies isolated.

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
Install all required libraries from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys
You need to tell the bot who you are. **Do not** hardcode keys in the Python files.

1.  Create a file named `.env` in the root directory.
2.  Paste your Binance Testnet credentials inside:

```text
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_secret_key_here
```



---

## 💻 How to Use

The bot is command-driven. Type `python main.py --help` to see all available commands.

### 1. Check Your Balance
See your available USDT and open positions before trading.

```bash
python main.py balance
```

**Output:**
```text
==============================
ACCOUNT BALANCE
==============================
💵 Wallet Balance: 5000.00 USDT
✅ Available Balance: 5000.00 USDT
------------------------------
No open positions.
==============================
```

### 2. Place a Market Order (Buy)
Buys the asset immediately at the current market price.

*   **Syntax:** `python main.py trade <SYMBOL> <SIDE> MARKET <QUANTITY>`
*   **Example:** Buy 0.002 Bitcoin.

```bash
python main.py trade BTCUSDT BUY MARKET 0.002
```

**Output:**
```text
==============================
ORDER SUMMARY
==============================
✅ Order Status: FILLED
🆔 Order ID: 13020059046
📊 Symbol: BTCUSDT
📈 Side: BUY
📝 Type: MARKET
📦 Executed Qty: 0.0020
💰 Avg Price: 66948.10
💵 Cost (USDT): 133.90
==============================
```

### 3. Place a Limit Order (Sell)
Sets a "target price." The order only executes if the market reaches that price.

*   **Syntax:** `python main.py trade <SYMBOL> <SIDE> LIMIT <QUANTITY> --price <TARGET_PRICE>`
*   **Example:** Sell 0.002 Bitcoin if the price hits $100,000.

```bash
python main.py trade BTCUSDT SELL LIMIT 0.002 --price 100000
```

---

## 🛠 Project Architecture

The code is structured using the **Separation of Concerns** principle, making it easy to maintain and test.

```text
binance-futures-trading-bot/
│
├── bot/                    # Core Logic
│   ├── __init__.py
│   ├── client.py           # Binance API Connection Wrapper
│   ├── orders.py           # Order Placement & Polling Logic
│   ├── validators.py       # Input Validation (Lot Size, Step Size)
│   └── logger.py           # Logging Configuration
│
├── logs/                   # Auto-generated logs
│   └── trading_bot.log
│
├── main.py                 # CLI Entry Point (Typer)
├── requirements.txt        # Dependencies
├── .env                    # API Keys (Do not commit)
└── README.md
```

### Key Components Explained

1.  **`client.py`**: Handles the connection to Binance. It ensures we connect to the **Testnet** URL, not the real market.
2.  **`validators.py`**: This is the brain. It asks Binance "What are the rules for BTC?" and rounds your inputs to match (e.g., preventing you from sending 0.00001 BTC if the minimum is 0.001).
3.  **`orders.py`**: Handles the "Do it" logic. It sends the order and then **waits 1 second** to check the result, ensuring you get the real fill price.

---

## ❓ Troubleshooting & FAQ

### Error: "Order's notional must be no smaller than 100"
**Meaning:** Your order is too small. Binance requires the *total value* of the trade to be at least 100 USDT.
*   **Fix:** Increase your quantity.
    *   For BTC (~$65k), use **0.002** or more.
    *   For ETH (~$3.5k), use **0.04** or more.

### Error: "Quantity less than or equal to zero"
**Meaning:** The validator rounded your input down to zero because the precision was wrong.
*   **Fix:** Check the `step_size` for the coin in the logs and increase your input quantity.

### Error: "No such command 'BTCUSDT'"
**Meaning:** You forgot the `trade` keyword.
*   **Fix:** Use `python main.py trade BTCUSDT ...`

---

## 🧪 Test Cases

To verify the bot is working correctly, try running these commands in sequence:

1.  **Check Balance:** `python main.py balance`
2.  **Market Buy (BTC):** `python main.py trade BTCUSDT BUY MARKET 0.002`
3.  **Market Buy (ETH):** `python main.py trade ETHUSDT BUY MARKET 0.04`
4.  **Limit Sell (BTC):** `python main.py trade BTCUSDT SELL LIMIT 0.002 --price 100000`
5.  **Check Balance:** `python main.py balance` (See your open positions).

---

## 📜 License

This project is open source and available for educational purposes.

---

**Built with ❤️ for Python Developers.**
```
