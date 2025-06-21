# 🚀 Binance Futures Testnet Trading Bot

A web-based trading interface for placing Market and Limit orders on the Binance Futures Testnet. Built with FastAPI, HTML/CSS, and the python-binance library.

## ✨ Features

- 📊 **Interactive Trading Interface**: Clean, responsive web interface for placing orders
- 🔄 **Market & Limit Orders**: Support for both market and limit order types
- 🛡️ **Input Validation**: Comprehensive client and server-side validation
- 📝 **Detailed Logging**: All trades and errors logged with timestamps
- 🎯 **Real-time Results**: Immediate feedback on order execution
- 📱 **Mobile Responsive**: Works seamlessly on desktop and mobile devices
- ⚠️ **Testnet Safe**: Uses Binance Futures Testnet - no real money involved

## 🏗️ Project Structure

```
binance_trading_app/
│
├── app/
│   ├── templates/
│   │   ├── index.html        # Home page with trade form
│   │   └── result.html       # Trade result page
│   ├── static/
│   │   └── style.css         # CSS styling
│   ├── main.py               # FastAPI application
│   ├── binance_client.py     # Binance API interaction
│   └── logger.py             # Logging configuration
│
├── .env                      # Environment variables (create from .env.example)
├── requirements.txt          # Python dependencies
├── Procfile                  # Railway deployment configuration
└── README.md                 # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Binance Futures Testnet account and API keys

### 1. Get Binance Testnet API Keys

1. Visit [Binance Futures Testnet](https://testnet.binancefuture.com/)
2. Create an account or log in
3. Generate API Key and Secret
4. **Important**: Keep your API credentials secure and never share them

### 2. Local Development Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd binance_trading_app

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Edit .env file with your API credentials
# API_KEY=your_binance_testnet_api_key
# API_SECRET=your_binance_testnet_secret

# Run the application
uvicorn app.main:app --reload
```

Visit `http://localhost:8000` to access the trading interface.

### 3. Railway Deployment

#### Step 1: Prepare for Deployment

1. Create a Railway account at [railway.app](https://railway.app)
2. Install Railway CLI:
   ```bash
   npm install -g @railway/cli
   ```
3. Login to Railway:
   ```bash
   railway login
   ```

#### Step 2: Deploy

1. Initialize Railway project:
   ```bash
   railway init
   ```

2. Set environment variables:
   ```bash
   railway variables set API_KEY=your_binance_testnet_api_key
   railway variables set API_SECRET=your_binance_testnet_secret
   ```

3. Deploy the application:
   ```bash
   railway up
   ```

4. Your app will be available at the provided Railway URL.

## 📖 Usage Guide

### Placing Orders

1. **Navigate to the trading interface**
2. **Fill out the order form**:
   - **Symbol**: Enter trading pair (e.g., `BTCUSDT`, `ETHUSDT`)
   - **Quantity**: Enter order quantity (minimum 0.0001)
   - **Order Type**: Select Market or Limit
   - **Side**: Choose Buy or Sell
   - **Price**: Required for limit orders only

3. **Submit the order**
4. **View results** on the result page

### Order Types

- **Market Orders**: Execute immediately at current market price
- **Limit Orders**: Execute only at specified price or better

### Supported Symbols

All Binance Futures symbols are supported. Popular examples:
- `BTCUSDT` - Bitcoin/USDT
- `ETHUSDT` - Ethereum/USDT
- `ADAUSDT` - Cardano/USDT
- `DOTUSDT` - Polkadot/USDT

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `API_KEY` | Binance Futures Testnet API Key | Yes |
| `API_SECRET` | Binance Futures Testnet Secret Key | Yes |

### Logging

All trades and errors are logged to `logs/trade_logs.log` with the following information:
- Timestamp
- Trade parameters
- API responses
- Error details

## 🛡️ Security Notes

- **Testnet Only**: This application is designed for Binance Futures Testnet
- **API Keys**: Never commit API keys to version control
- **Environment Variables**: Use `.env` file locally and environment variables in production
- **No Real Money**: Testnet uses fake money for testing purposes

## 🔍 API Endpoints

### `GET /`
- **Description**: Renders the home page with trading form
- **Response**: HTML page

### `POST /place_order`
- **Description**: Processes trade form and places order
- **Parameters**:
  - `symbol` (string): Trading pair
  - `quantity` (float): Order quantity
  - `order_type` (string): "MARKET" or "LIMIT"
  - `side` (string): "BUY" or "SELL"
  - `price` (float, optional): Price for limit orders
- **Response**: HTML page with results

## 🐛 Troubleshooting

### Common Issues

1. **"Invalid symbol" error**
   - Ensure symbol is uppercase (e.g., `BTCUSDT`)
   - Check if symbol exists on Binance Futures

2. **"Insufficient balance" error**
   - Your testnet account needs balance
   - Get testnet funds from Binance Futures Testnet

3. **"MIN_NOTIONAL" error**
   - Order value is too small
   - Increase quantity or price

4. **Connection errors**
   - Check your internet connection
   - Verify API keys are correct

### Logs

Check `logs/trade_logs.log` for detailed error information and debugging.

## 🔄 Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

### Code Structure

- **`main.py`**: FastAPI application with routes and validation
- **`binance_client.py`**: Binance API interaction wrapper
- **`logger.py`**: Logging configuration and utilities
- **`templates/`**: Jinja2 HTML templates
- **`static/`**: CSS and static assets

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## ⚠️ Disclaimer

This software is for educational and testing purposes only. It uses Binance Futures Testnet which involves no real money. Always exercise caution when trading with real funds and never risk more than you can afford to lose.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs in `logs/trade_logs.log`
3. Create an issue on GitHub

---

**Happy Trading! 📈**

*Remember: This is a testnet application. No real money is involved.*