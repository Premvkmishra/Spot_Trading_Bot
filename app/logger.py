import logging
import os
from datetime import datetime

def setup_logger():
    """
    Setup logging configuration for the trading application
    
    Returns:
        logging.Logger: Configured logger instance
    """
    
    # Create logs directory if it doesn't exist
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Create logger
    logger = logging.getLogger('binance_trading_bot')
    logger.setLevel(logging.INFO)
    
    # Avoid adding multiple handlers if logger already exists
    if not logger.handlers:
        # Create file handler
        log_file = os.path.join(log_dir, 'trade_logs.log')
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Add formatter to handlers
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger

def log_trade_attempt(logger, trade_data):
    """Log trade attempt with structured data"""
    logger.info(f"=== TRADE ATTEMPT ===")
    logger.info(f"Timestamp: {datetime.now().isoformat()}")
    logger.info(f"Symbol: {trade_data.get('symbol')}")
    logger.info(f"Side: {trade_data.get('side')}")
    logger.info(f"Type: {trade_data.get('order_type')}")
    logger.info(f"Quantity: {trade_data.get('quantity')}")
    if trade_data.get('price'):
        logger.info(f"Price: {trade_data.get('price')}")
    logger.info("=====================")

def log_trade_result(logger, success, result_data):
    """Log trade result with structured data"""
    logger.info(f"=== TRADE RESULT ===")
    logger.info(f"Timestamp: {datetime.now().isoformat()}")
    logger.info(f"Success: {success}")
    
    if success:
        logger.info(f"Order ID: {result_data.get('orderId')}")
        logger.info(f"Status: {result_data.get('status')}")
        logger.info(f"Executed Quantity: {result_data.get('executedQty')}")
        if result_data.get('avgPrice'):
            logger.info(f"Average Price: {result_data.get('avgPrice')}")
    else:
        logger.error(f"Error: {result_data}")
    
    logger.info("====================")

def log_error(logger, error_message, error_details=None):
    """Log error with details"""
    logger.error(f"=== ERROR ===")
    logger.error(f"Timestamp: {datetime.now().isoformat()}")
    logger.error(f"Message: {error_message}")
    if error_details:
        logger.error(f"Details: {error_details}")
    logger.error("=============")

# Example usage
if __name__ == "__main__":
    # Test logger setup
    test_logger = setup_logger()
    test_logger.info("Logger setup successful")
    
    # Test structured logging
    test_trade_data = {
        'symbol': 'BTCUSDT',
        'side': 'BUY',
        'order_type': 'MARKET',
        'quantity': 0.001
    }
    
    log_trade_attempt(test_logger, test_trade_data)
    log_trade_result(test_logger, True, {'orderId': '12345', 'status': 'FILLED'})
    log_error(test_logger, "Test error message", "Additional error details")