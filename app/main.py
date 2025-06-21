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
    price: Optional[float] = Form(None)
):
    """Process trade form submission and place order"""
    
    # Validation
    errors = []
    
    # Validate symbol
    if not validate_symbol(symbol):
        errors.append("Invalid symbol format. Use uppercase format like BTCUSDT")
    
    # Validate quantity
    if not validate_quantity(quantity):
        errors.append("Quantity must be positive and at least 0.0001")
    
    # Validate price for limit orders
    if not validate_price(price, order_type):
        errors.append("Price is required for limit orders and must be positive")
    
    # Validate order type and side
    if order_type.upper() not in ["MARKET", "LIMIT"]:
        errors.append("Order type must be MARKET or LIMIT")
    
    if side.upper() not in ["BUY", "SELL"]:
        errors.append("Side must be BUY or SELL")
    
    # If validation errors, return to form with errors
    if errors:
        logger.warning(f"Validation errors: {errors}")
        return templates.TemplateResponse(
            "index.html", 
            {"request": request, "errors": errors}
        )
    
    # Log the trade attempt
    trade_data = {
        "symbol": symbol.upper(),
        "quantity": quantity,
        "order_type": order_type.upper(),
        "side": side.upper(),
        "price": price
    }
    logger.info(f"Trade attempt: {trade_data}")
    
    try:
        # Place the order
        order_response = binance_client.place_order(
            symbol=symbol.upper(),
            quantity=quantity,
            order_type=order_type.upper(),
            side=side.upper(),
            price=price
        )
        
        logger.info(f"Order successful: {order_response}")
        
        return templates.TemplateResponse(
            "result.html",
            {
                "request": request,
                "success": True,
                "order_response": order_response,
                "trade_data": trade_data
            }
        )
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Order failed: {error_msg}")
        
        # Map common Binance errors to user-friendly messages
        if "Invalid symbol" in error_msg:
            error_msg = "Invalid trading symbol. Please check the symbol name."
        elif "Insufficient balance" in error_msg:
            error_msg = "Insufficient balance for this order."
        elif "MIN_NOTIONAL" in error_msg:
            error_msg = "Order value is too small. Please increase quantity or price."
        elif "PRICE_FILTER" in error_msg:
            error_msg = "Price is outside allowed range for this symbol."
        
        return templates.TemplateResponse(
            "result.html",
            {
                "request": request,
                "success": False,
                "error_message": error_msg,
                "trade_data": trade_data
            }
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)