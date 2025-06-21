import os
from dotenv import load_dotenv
from binance.client import Client
import time

load_dotenv()
client = Client(os.getenv('API_KEY'), os.getenv('API_SECRET'), testnet=True)
client.API_URL = 'https://testnet.binance.vision/api'

# Sync time with server
server_time = client.get_server_time()
local_time = int(time.time() * 1000)
time_offset = server_time['serverTime'] - local_time
client.timestamp_offset = time_offset

try:
    # Get all open orders
    open_orders = client.get_open_orders()
    
    print(f"=== Current Open Orders ({len(open_orders)}) ===")
    
    if not open_orders:
        print("No open orders found!")
    else:
        for i, order in enumerate(open_orders, 1):
            print(f"\n{i}. Order ID: {order['orderId']}")
            print(f"   Symbol: {order['symbol']}")
            print(f"   Side: {order['side']}")
            print(f"   Type: {order['type']}")
            print(f"   Quantity: {order['origQty']}")
            print(f"   Status: {order['status']}")
            if order.get('price'):
                print(f"   Price: ${order['price']}")
            if order.get('stopPrice'):
                print(f"   Stop Price: ${order['stopPrice']}")
            print(f"   Time: {order['time']}")
    
    print(f"\n=== Account Info ===")
    account = client.get_account()
    print(f"Total Orders: {len(account['orders'])}")
    
except Exception as e:
    print(f"Error: {e}") 