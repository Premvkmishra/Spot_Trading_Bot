# Deployment Guide

## Railway Deployment

1. **Connect your GitHub repository to Railway**
2. **Set Environment Variables:**
   - `API_KEY`: Your Binance Spot Testnet API Key
   - `API_SECRET`: Your Binance Spot Testnet API Secret
3. **Deploy automatically**

## Render Deployment

1. **Create a new Web Service**
2. **Connect your GitHub repository**
3. **Set Environment Variables:**
   - `API_KEY`: Your Binance Spot Testnet API Key
   - `API_SECRET`: Your Binance Spot Testnet API Secret
4. **Build Command:** `pip install -r requirements.txt`
5. **Start Command:** `bash start.sh`
6. **Or use the render.yaml file for automatic configuration**

## Heroku Deployment

1. **Install Heroku CLI**
2. **Login and create app:**
   ```bash
   heroku login
   heroku create your-app-name
   ```
3. **Set environment variables:**
   ```bash
   heroku config:set API_KEY=your_api_key
   heroku config:set API_SECRET=your_api_secret
   ```
4. **Deploy:**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

## Important Notes

- **Never commit your `.env` file** - it contains sensitive API keys
- **Use Binance Spot Testnet** for testing (not mainnet)
- **Get API keys from:** https://testnet.binance.vision/
- **The app runs on port 8000** locally and uses `$PORT` on deployment platforms
- **Uses Uvicorn ASGI server** (not Gunicorn) 