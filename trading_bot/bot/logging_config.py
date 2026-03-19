import logging
import os

def setup_logging():
    log_format = '%(asctime)s [%(levelname)s] %(message)s'
    base_dir = os.path.dirname(os.path.dirname(__file__))
    
    formatter = logging.Formatter(log_format)
    
    # 1. General Application Logger (Console)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    if logger.hasHandlers():
        logger.handlers.clear()
        
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 2. Error Logger
    error_logger = logging.getLogger('errors')
    error_logger.setLevel(logging.ERROR)
    error_handler = logging.FileHandler(os.path.join(base_dir, 'errors.log'))
    error_handler.setFormatter(formatter)
    error_logger.addHandler(error_handler)
    error_logger.propagate = True
    
    # Capture all root errors into errors.log as well
    class ErrorFilter(logging.Filter):
        def filter(self, record):
            if record.levelno >= logging.ERROR:
                error_handler.emit(record)
            return True
            
    logger.addFilter(ErrorFilter())
    
    # 3. Orders Logger
    orders_logger = logging.getLogger('orders')
    orders_logger.setLevel(logging.INFO)
    orders_handler = logging.FileHandler(os.path.join(base_dir, 'orders.log'))
    orders_handler.setFormatter(formatter)
    orders_logger.addHandler(orders_handler)
    orders_logger.propagate = True

    # 4. Requests/Responses Logger
    requests_logger = logging.getLogger('requests')
    requests_logger.setLevel(logging.INFO)
    requests_handler = logging.FileHandler(os.path.join(base_dir, 'requests.log'))
    requests_handler.setFormatter(formatter)
    requests_logger.addHandler(requests_handler)
    requests_logger.propagate = True
    
    logging.info("Logging configured: orders.log, requests.log, errors.log initialized.")
