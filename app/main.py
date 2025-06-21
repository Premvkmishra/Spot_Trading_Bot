from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from .binance_client import BinanceClient
from .logger import setup_logger
import re
from typing import Optional

app = FastAPI(title="Binance Futures Testnet Trading Bot")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="app/templates")

# Initialize logger and Binance client
logger = setup_logger()
binance_client = BinanceClient()

def validate_symbol(symbol: str) -> bool:
    """Validate trading symbol format"""
    if not symbol:
        return False
    # Check if symbol is uppercase and matches typical format
    pattern = r'^[A-Z]{3,}USDT?$'
    return bool(re.match(pattern, symbol.upper()))

def validate_quantity(quantity: float) -> bool:
    """Validate order quantity"""
    return quantity > 0 and quantity >= 0.0001

def validate_price(price: Optional[float], order_type: str) -> bool:
    """Validate price for limit orders"""
    if order_type.upper() == "LIMIT":
        return price is not None and price > 0
    return True

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the home page with trading form"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/place_order", response_class=HTMLResponse)
async def place_order(
    request: Request,
    symbol: str = Form(...),
    quantity: float = Form(...),
    order_type: str = Form(...),
    side: str = Form(...),
    price: Optional[float] = Form(None),
    stop_price: Optional[float] = Form(None)
):
    """
    Place an order on Binance Vision Testnet
    """
    try:
        # Validate symbol format
        if not re.match(r'^[A-Z0-9]+$', symbol):
            raise HTTPException(status_code=400, detail="Invalid symbol format")
        
        # Validate order type
        if order_type not in ['MARKET', 'LIMIT', 'STOP_LIMIT']:
            raise HTTPException(status_code=400, detail="Invalid order type")
        
        # Validate side
        if side not in ['BUY', 'SELL']:
            raise HTTPException(status_code=400, detail="Invalid side")
        
        # Validate price requirements
        if order_type in ['LIMIT', 'STOP_LIMIT'] and price is None:
            raise HTTPException(status_code=400, detail="Price is required for LIMIT and STOP_LIMIT orders")
        
        # Validate stop price for Stop-Limit orders
        if order_type == 'STOP_LIMIT' and stop_price is None:
            raise HTTPException(status_code=400, detail="Stop price is required for STOP_LIMIT orders")
        
        # Log the trade attempt
        trade_data = {
            'symbol': symbol,
            'quantity': quantity,
            'order_type': order_type,
            'side': side,
            'price': price,
            'stop_price': stop_price
        }
        logger.info(f"Trade attempt: {trade_data}")
        
        # Place the order
        order_response = binance_client.place_order(
            symbol=symbol,
            quantity=quantity,
            order_type=order_type,
            side=side,
            price=price,
            stop_price=stop_price
        )
        
        # Log successful order
        logger.info(f"Order placed successfully: {order_response}")
        
        # Return success page
        return templates.TemplateResponse("result.html", {
            "request": request,
            "success": True,
            "order_response": order_response,
            "trade_data": trade_data
        })
        
    except Exception as e:
        # Log the error
        logger.error(f"Order failed: {str(e)}")
        
        # Return error page
        return templates.TemplateResponse("result.html", {
            "request": request,
            "success": False,
            "error_message": str(e),
            "trade_data": {
                'symbol': symbol,
                'quantity': quantity,
                'order_type': order_type,
                'side': side,
                'price': price,
                'stop_price': stop_price
            }
        })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)