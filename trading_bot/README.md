# Binance Futures Testnet Trading Bot

A simplified, robust Python trading bot that places Market and Limit orders on the Binance Futures Testnet (USDT-M). This repository contains the bot logic, a **Command-Line Interface (CLI)**, and a **Flask-based Web GUI**.

## Features
- **Binance Testnet Integration**: Uses `python-binance` to cleanly interface with the testnet.
- **Two Modalities**: 
  - Typer/Click-based CLI for terminal command usage.
  - Flask web application with a modern, dark-mode styling (Tailwind CSS) inspired by premium setups.
- **Validation Options**: Validate symbol format, order sides, types, and limits securely.
- **Mock Mode**: The bot defaults to generating robust mock logs if no API Keys are provided.

## Setup Steps

### 1. Requirements
- Python 3.9+
- A Binance Futures Testnet Account

### 2. Installation
Clone or extract the repository, then navigate to its root directory. Install the dependencies:
```bash
python -m pip install -r requirements.txt
```

### 3. API Keys Configuration (Optional, for Real Orders)
Create a `.env` file in the root directory (where `app.py` is located) with the following structure:
```env
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_api_secret_here
```
*(If no `.env` credentials are found, the application gracefully defaults to MOCK mode and will simulate successful testnet exchanges).*

## How to Run Examples

### 1. Command Line Interface (CLI)
You can use `cli.py` to fetch prices, get your balance, and place orders.

**View Available Commands:**
```bash
python cli.py --help
```

**Get Market Price:**
```bash
python cli.py price --symbol BTCUSDT
```

**Place a Limit Order:**
```bash
python cli.py order --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.5 --price 3500.0
```

**Place a Market Order:**
```bash
python cli.py order --symbol DOGEUSDT --side BUY --type MARKET --quantity 100
```

### 2. Flask Web GUI
To launch the modern browser interface:
```bash
python app.py
```
Then navigate to `http://127.0.0.1:5000` in your web browser. 
Select your pairs, pick your order size and leverage, then execute. Activity is automatically logged locally in the graphical display and system files.

## Log Output (`trading.log`)
Application activity including API interactions, errors, and mock placements are persisted automatically to `trading.log` within the root directory. Submit this file alongside the implementation if requested for auditing.

## Assumptions
- Real Binance execution on the testnet strictly requires both the `API_KEY` and the `API_SECRET`. Since an `API_SECRET` was not universally provided during setup, the code includes a smart Mock abstraction.
- It is assumed `USDT-M` contracts are the sole target (enforced inside the validators layer).
