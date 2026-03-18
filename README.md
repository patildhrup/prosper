# Binance Futures Trading Bot (Testnet)

A robust Python CLI tool for placing orders on the Binance Futures Testnet (USDT-M) with enhanced UI, logging, and error handling.

## Features
- **Order Types**: Support for `MARKET`, `LIMIT`, and `STOP_MARKET` (Bonus).
- **Sides**: `BUY` and `SELL`.
- **UI**: Premium CLI experience using `Rich` for tables, panels, and status spinners.
- **Logging**: Comprehensive logging of API requests, responses, and errors to `logs/trading.log`.
- **Validation**: Robust input validation for symbol, side, and order-specific parameters.

## Setup Instructions

### 1. Prerequisites
- Python 3.8+
- Binance Futures Testnet API Key and Secret Key.

### 2. Installation
Clone the repository and install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the root directory and add your credentials:
```env
BINANCE_API_KEY=your_testnet_api_key
BINANCE_SECRET_KEY=your_testnet_secret_key
# Optional: Override base URL if needed
# BASE_URL=https://testnet.binancefuture.com
```

## How to Run
Use the `cli.py` script to place orders.

### Place a MARKET Order
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --qty 0.001
```

### Place a LIMIT Order
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --qty 0.001 --price 60000
```

### Place a STOP_MARKET Order (Bonus)
```bash
python cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --qty 0.001 --stop 55000
```

## Implementation Details
- **Architecture**: Separated into `Bot/` (API logic & config) and `cli.py` (CLI interface).
- **Logging**: Powered by `loguru`. Logs are stored in the `logs/` directory with automatic rotation.
- **Error Handling**: Handles Binance API exceptions, network issues, and invalid user inputs with clear feedback.

## Assumptions
- The bot assumes the user has sufficient margin/balance in their Testnet account.
- Symbols should be provided in standard Binance format (e.g., `BTCUSDT`).
- Quantity and Price must be valid for the specific symbol's filters (precision, min/max).
