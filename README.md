# Binance Futures Trading Bot (Testnet)

A robust Python CLI tool for placing orders on the Binance Futures Testnet (USDT-M) with enhanced UI, logging, and error handling.

## Features
- **Interactive Mode**: User-friendly menu-driven interface that stays open for multiple orders.
- **Order Types**: Support for `MARKET`, `LIMIT`, and `STOP_MARKET` (Bonus).
- **Sides**: `BUY` and `SELL`.
- **UI**: Premium CLI experience using `Rich` and `Questionary`.
- **Logging**: Comprehensive logging of API requests, responses, and errors to `logs/trading.log`.
- **Validation**: Robust input validation for symbol, side, and order-specific parameters.

## Setup Instructions

### 1. Prerequisites
- Python 3.8+
- Binance Futures Testnet API Key and Secret Key.

### 2. Installation
Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the `Trading-Bot/` directory and add your credentials:
```env
BINANCE_API_KEY=your_testnet_api_key
BINANCE_SECRET_KEY=your_testnet_secret_key
# BASE_URL=https://testnet.binancefuture.com
```

## How to Run

### Interactive Mode (Recommended for non-technical users)
Simply run the script without any arguments. It will guide you through the process and stay open until you choose to exit.
```bash
python cli.py
```

### Command Line Mode (For technical users/scripts)
Place a one-off order using flags:
```bash
# MARKET Order
python cli.py --symbol BTCUSDT --side BUY --type MARKET --qty 0.1

# LIMIT Order
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --qty 0.1 --price 150000

# STOP_MARKET Order
python cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --qty 0.1 --stop 50000
```

## Implementation Details
- **Main Loop**: The interactive mode uses a `while True` loop to allow continuous execution.
- **Architecture**: Separated into `Bot/` (API logic & config) and `cli.py` (CLI interface).
- **Logging**: Powered by `loguru`. Logs are stored in the `logs/` directory.
- **Error Handling**: Handles Binance API exceptions and invalid user inputs with clear feedback.

## Assumptions
- Symbols should be provided in standard Binance format (e.g., `BTCUSDT`).
- Quantity and Price must be valid for the specific symbol's filters (notional >= 5.0, etc.).
