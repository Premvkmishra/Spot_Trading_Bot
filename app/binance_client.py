from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
import os
from dotenv import load_dotenv
from typing import Optional, Dict, Any
import time

# Load environment variables
print("Current working directory:", os.getcwd())
print("Looking for .env file...")
load_dotenv()

class BinanceClient:
    def __init__(self):
        """Initialize Binance client with Vision testnet configuration"""
        self.api_key = os.getenv('API_KEY')
        self.api_secret = os.getenv('API_SECRET')
        
        print(f"API_KEY loaded: {self.api_key[:10] if self.api_key else 'None'}...")
        print(f"API_SECRET loaded: {self.api_secret[:10] if self.api_secret else 'None'}...")
        
        if not self.api_key or not self.api_secret:
            raise ValueError("API_KEY and API_SECRET must be set in .env file")
        
        # Initialize client for Vision testnet (spot trading)
        self.client = Client(
            api_key=self.api_key,
            api_secret=self.api_secret,
            testnet=True
        )
        
        # Set to Vision testnet API URL
        self.client.API_URL = 'https://testnet.binance.vision/api'
        
        print(f"Using API URL: {self.client.API_URL}")
        print(f"Testnet mode: {self.client.testnet}")
        
        # Sync time with Binance server
        self._sync_time()
    
    def _sync_time(self):
        """Synchronize local time with Binance server time"""
        try:
            server_time = self.client.get_server_time()
            local_time = int(time.time() * 1000)
            time_offset = server_time['serverTime'] - local_time
            
            print(f"Local time: {local_time}")
            print(f"Server time: {server_time['serverTime']}")
            print(f"Time offset: {time_offset}ms")
            
            # Set the time offset for future requests
            self.client.timestamp_offset = time_offset
            
            # Also set the timestamp directly on the client
            if hasattr(self.client, '_timestamp'):
                self.client._timestamp = time_offset
            
            print(f"Time synchronized. Offset set to: {time_offset}ms")
            
        except Exception as e:
            print(f"Warning: Could not sync time with Binance server: {e}")
            # Continue without time sync
    
    def place_order(
        self, 
        symbol: str, 
        quantity: float, 
        order_type: str, 
        side: str, 
        price: Optional[float] = None,
        stop_price: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Place an order on Binance Vision Testnet (Spot Trading)
        
        Args:
            symbol: Trading pair (e.g., 'BTCUSDT')
            quantity: Order quantity
            order_type: 'MARKET', 'LIMIT', or 'STOP_LIMIT'
            side: 'BUY' or 'SELL'
            price: Price for limit orders (optional for market orders)
            stop_price: Stop price for stop-limit orders (required for STOP_LIMIT)
        
        Returns:
            Dict containing order response
        
        Raises:
            BinanceAPIException: If API call fails
            ValueError: If invalid parameters provided
        """
        print(f"Placing order with API_KEY: {self.api_key[:10]}...")
        print(f"Order details: {symbol}, {quantity}, {order_type}, {side}, price={price}, stop_price={stop_price}")
        
        try:
            # Validate inputs
            if not symbol or not quantity or not order_type or not side:
                raise ValueError("All parameters are required")
            
            if order_type not in ['MARKET', 'LIMIT', 'STOP_LIMIT']:
                raise ValueError("Order type must be 'MARKET', 'LIMIT', or 'STOP_LIMIT'")
            
            if side not in ['BUY', 'SELL']:
                raise ValueError("Side must be 'BUY' or 'SELL'")
            
            if order_type in ['LIMIT', 'STOP_LIMIT'] and not price:
                raise ValueError("Price is required for LIMIT and STOP_LIMIT orders")
            
            if order_type == 'STOP_LIMIT' and not stop_price:
                raise ValueError("Stop price is required for STOP_LIMIT orders")
            
            # Use the correct Spot trading methods
            if order_type == "MARKET":
                if side == "BUY":
                    response = self.client.order_market_buy(
                        symbol=symbol,
                        quantity=quantity
                    )
                else:  # SELL
                    response = self.client.order_market_sell(
                        symbol=symbol,
                        quantity=quantity
                    )
            elif order_type == "LIMIT":
                if price is None:
                    raise ValueError("Price is required for limit orders")
                
                if side == "BUY":
                    response = self.client.order_limit_buy(
                        symbol=symbol,
                        quantity=quantity,
                        price=price,
                        timeInForce='GTC'
                    )
                else:  # SELL
                    response = self.client.order_limit_sell(
                        symbol=symbol,
                        quantity=quantity,
                        price=price,
                        timeInForce='GTC'
                    )
            elif order_type == "STOP_LIMIT":
                if price is None or stop_price is None:
                    raise ValueError("Both price and stop_price are required for stop-limit orders")
                
                # For Stop-Limit orders, we use the generic order method
                order_params = {
                    'symbol': symbol,
                    'side': side,
                    'type': 'STOP_LOSS_LIMIT',
                    'quantity': quantity,
                    'price': price,
                    'stopPrice': stop_price,
                    'timeInForce': 'GTC'
                }
                
                response = self.client.create_order(**order_params)
            else:
                raise ValueError("Invalid order type. Must be 'MARKET', 'LIMIT', or 'STOP_LIMIT'")
            
            print(f"Order placed successfully: {response}")
            return response
            
        except BinanceAPIException as e:
            # Handle timestamp errors specifically
            if e.code == -1021:  # Timestamp error
                # Try to resync time and retry once
                try:
                    self._sync_time()
                    # Retry the order with synced time
                    if order_type == "MARKET":
                        if side == "BUY":
                            response = self.client.order_market_buy(
                                symbol=symbol,
                                quantity=quantity
                            )
                        else:  # SELL
                            response = self.client.order_market_sell(
                                symbol=symbol,
                                quantity=quantity
                            )
                    elif order_type == "LIMIT":
                        if side == "BUY":
                            response = self.client.order_limit_buy(
                                symbol=symbol,
                                quantity=quantity,
                                price=price,
                                timeInForce='GTC'
                            )
                        else:  # SELL
                            response = self.client.order_limit_sell(
                                symbol=symbol,
                                quantity=quantity,
                                price=price,
                                timeInForce='GTC'
                            )
                    elif order_type == "STOP_LIMIT":
                        order_params = {
                            'symbol': symbol,
                            'side': side,
                            'type': 'STOP_LOSS_LIMIT',
                            'quantity': quantity,
                            'price': price,
                            'stopPrice': stop_price,
                            'timeInForce': 'GTC'
                        }
                        response = self.client.create_order(**order_params)
                    
                    print(f"Order placed successfully after time sync: {response}")
                    return response
                except BinanceAPIException as retry_e:
                    print(f"Order failed after time sync retry: {retry_e}")
                    raise retry_e
            else:
                print(f"Order failed: {e}")
                raise e
        except Exception as e:
            print(f"Unexpected error placing order: {e}")
            raise e
    
    def get_account_info(self) -> Dict[str, Any]:
        """Get spot account information"""
        try:
            return self.client.get_account()
        except Exception as e:
            raise Exception(f"Failed to get account info: {str(e)}")
    
    def get_symbol_info(self, symbol: str) -> Dict[str, Any]:
        """Get symbol information"""
        try:
            exchange_info = self.client.get_exchange_info()
            for s in exchange_info['symbols']:
                if s['symbol'] == symbol:
                    return s
            raise Exception(f"Symbol {symbol} not found")
        except Exception as e:
            raise Exception(f"Failed to get symbol info: {str(e)}")
    
    def test_connectivity(self) -> bool:
        """Test connection to Binance API"""
        try:
            self.client.ping()
            return True
        except Exception:
            return False
    
    def get_balance(self, asset: str = None) -> Dict[str, Any]:
        """Get account balance for specific asset or all assets"""
        try:
            account_info = self.client.get_account()
            if asset:
                for balance in account_info['balances']:
                    if balance['asset'] == asset:
                        return balance
                return {'asset': asset, 'free': '0.00000000', 'locked': '0.00000000'}
            return account_info['balances']
        except Exception as e:
            raise Exception(f"Failed to get balance: {str(e)}")
    
    def get_ticker_price(self, symbol: str = None) -> Dict[str, Any]:
        """Get current price for symbol or all symbols"""
        try:
            if symbol:
                return self.client.get_symbol_ticker(symbol=symbol)
            return self.client.get_all_tickers()
        except Exception as e:
            raise Exception(f"Failed to get ticker price: {str(e)}")
    
    def get_order_book(self, symbol: str, limit: int = 100) -> Dict[str, Any]:
        """Get order book for a symbol"""
        try:
            return self.client.get_order_book(symbol=symbol, limit=limit)
        except Exception as e:
            raise Exception(f"Failed to get order book: {str(e)}")
    
    def cancel_order(self, symbol: str, order_id: int) -> Dict[str, Any]:
        """Cancel an existing order"""
        try:
            return self.client.cancel_order(symbol=symbol, orderId=order_id)
        except Exception as e:
            raise Exception(f"Failed to cancel order: {str(e)}")
    
    def get_open_orders(self, symbol: str = None) -> Dict[str, Any]:
        """Get all open orders or open orders for a specific symbol"""
        try:
            if symbol:
                return self.client.get_open_orders(symbol=symbol)
            return self.client.get_open_orders()
        except Exception as e:
            raise Exception(f"Failed to get open orders: {str(e)}")