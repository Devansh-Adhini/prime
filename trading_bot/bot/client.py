import os
import logging
from binance import Client
from dotenv import load_dotenv

load_dotenv()

_mock_mode = False
_client_instance = None

def get_client(mock: bool = False):
    global _client_instance
    global _mock_mode
    
    if _client_instance is None:
        _mock_mode = mock
        api_key = os.getenv('BINANCE_API_KEY', '')
        api_secret = os.getenv('BINANCE_API_SECRET', '')

        if not api_key or not api_secret:
            logging.warning("BINANCE_API_KEY or BINANCE_API_SECRET not found in environment. Defaulting to MOCK mode.")
            _mock_mode = True

        # Initialize the python-binance Client
        _client_instance = Client(api_key, api_secret, testnet=True)
        # Force the Futures URL to the testnet URL explicitly (although testnet=True might do it)
        _client_instance.FUTURES_URL = 'https://testnet.binancefuture.com'
        
        logging.info(f"Binance Client initialized. MOCK mode: {_mock_mode}")

    return _client_instance

def is_mock():
    return _mock_mode
