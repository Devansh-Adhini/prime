import logging
from binance.exceptions import BinanceAPIException
import requests

from .client import get_client, is_mock
from .validators import (
    validate_symbol,
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price
)

# Use dedicated loggers
logger = logging.getLogger('orders')
req_logger = logging.getLogger('requests')
err_logger = logging.getLogger('errors')

def get_market_price(symbol: str) -> float:
    try:
        symbol = validate_symbol(symbol)
        resp = requests.get(
            "https://testnet.binancefuture.com/fapi/v1/ticker/price",
            params={"symbol": symbol},
            timeout=5
        )
        resp.raise_for_status()
        data = resp.json()
        price = float(data["price"])
        return price
    except Exception as e:
        err_logger.error(f"Error fetching public price for {symbol}: {e}")
        return 0.0

def get_balance() -> float:
    client = get_client()
    if is_mock():
        return 10000.0
    
    try:
        bal = client.futures_account_balance()
        for entry in bal:
            if entry['asset'] == 'USDT':
                return float(entry['balance'])
        return 0.0
    except BinanceAPIException as e:
        err_logger.error(f"Binance API error fetching balance: {e.message}")
        return 0.0
    except Exception as e:
        err_logger.error(f"Error fetching balance: {e}")
        return 0.0

def place_order(symbol: str, side: str, order_type: str, quantity: float, price: float = None):
    try:
        # Validate Inputs
        symbol = validate_symbol(symbol)
        side = validate_side(side)
        order_type = validate_order_type(order_type)
        quantity = validate_quantity(quantity)
        
        if order_type == "LIMIT":
            price = validate_price(price, order_type)

        params = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'quantity': quantity,
        }
        
        req_logger.info(f"REQ [place_order]: {params}")

        client = get_client()

        if is_mock():
            import uuid
            mock_order_id = int(uuid.uuid4().int % 100000000)
            mock_resp = {
                "orderId": mock_order_id,
                "symbol": symbol,
                "status": "NEW" if order_type == "LIMIT" else "FILLED",
                "clientOrderId": f"mock_{mock_order_id}",
                "price": str(price) if price else "0",
                "avgPrice": str(price) if price else "50000.0",
                "origQty": str(quantity),
                "executedQty": "0" if order_type == "LIMIT" else str(quantity),
                "cumQuote": "0",
                "timeInForce": "GTC" if order_type == "LIMIT" else "GTC",
                "type": order_type,
                "side": side
            }
            req_logger.info(f"RES [place_order]: {mock_resp}")
            logger.info(f"MOCK Order Placed: {side} {quantity} {symbol} @ {price or 'MARKET'}")
            return True, mock_resp

        # Actual API Call
        order = client.futures_create_order(**params)
        req_logger.info(f"RES [place_order]: {order}")
        logger.info(f"Order Placed: {side} {quantity} {symbol} @ {price or 'MARKET'} (ID: {order.get('orderId')})")
        return True, order

    except ValueError as ve:
        err_msg = f"Validation Error: {str(ve)}"
        err_logger.error(err_msg)
        return False, {"error": err_msg}
    except BinanceAPIException as api_err:
        err_msg = f"Binance API Error: {api_err.message} (Code: {api_err.code})"
        err_logger.error(err_msg)
        return False, {"error": err_msg}
    except Exception as e:
        err_msg = f"Unexpected Error: {str(e)}"
        err_logger.exception(err_msg)
        return False, {"error": err_msg}

def get_open_orders(symbol: str) -> list:
    client = get_client()
    if is_mock():
        return []
    try:
        symbol = validate_symbol(symbol)
        orders = client.futures_get_open_orders(symbol=symbol)
        return orders
    except BinanceAPIException as e:
        logger.error(f"Binance API error fetching open orders: {e.message}")
        return []
    except Exception as e:
        logger.error(f"Error fetching open orders: {e}")
        return []

def cancel_order(symbol: str, order_id: int) -> tuple[bool, dict]:
    client = get_client()
    if is_mock():
        req_logger.info(f"REQ [cancel_order]: symbol={symbol}, orderId={order_id}")
        mock_resp = {"orderId": order_id, "status": "CANCELED"}
        req_logger.info(f"RES [cancel_order]: {mock_resp}")
        logger.info(f"MOCK Order Canceled: ID {order_id} on {symbol}")
        return True, mock_resp
    try:
        symbol = validate_symbol(symbol)
        req_logger.info(f"REQ [cancel_order]: symbol={symbol}, orderId={order_id}")
        response = client.futures_cancel_order(symbol=symbol, orderId=order_id)
        req_logger.info(f"RES [cancel_order]: {response}")
        logger.info(f"Order Canceled: ID {order_id} on {symbol}")
        return True, response
    except BinanceAPIException as e:
        err_msg = f"Binance API Error canceling order: {e.message}"
        err_logger.error(err_msg)
        return False, {"error": err_msg}
    except Exception as e:
        err_msg = f"Unexpected Error canceling order: {str(e)}"
        err_logger.error(err_msg)
        return False, {"error": err_msg}

def get_positions(symbol: str = None) -> list:
    client = get_client()
    if is_mock():
        return []
    try:
        positions = client.futures_position_information()
        if symbol:
            symbol = validate_symbol(symbol)
            positions = [p for p in positions if p['symbol'] == symbol]
        return [p for p in positions if float(p['positionAmt']) != 0]
    except BinanceAPIException as e:
        logger.error(f"Binance API error fetching positions: {e.message}")
        return []
    except Exception as e:
        logger.error(f"Error fetching positions: {e}")
        return []

def close_position(symbol: str) -> tuple[bool, dict]:
    client = get_client()
    if is_mock():
        req_logger.info(f"REQ [close_position]: symbol={symbol}")
        mock_resp = {"status": "MOCK_CLOSED"}
        req_logger.info(f"RES [close_position]: {mock_resp}")
        logger.info(f"MOCK Position Closed for {symbol}")
        return True, mock_resp
    try:
        symbol = validate_symbol(symbol)
        positions = get_positions(symbol)
        if not positions:
            return False, {"error": f"No active position found for {symbol}"}
        
        pos = positions[0]
        amt = float(pos['positionAmt'])
        if amt == 0:
            return False, {"error": "Position amount is 0"}
            
        side = 'BUY' if amt < 0 else 'SELL'
        quantity = abs(amt)
        
        req_logger.info(f"REQ [close_position]: symbol={symbol}, side={side}, quantity={quantity}, reduceOnly=True")
        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type='MARKET',
            quantity=quantity,
            reduceOnly=True
        )
        req_logger.info(f"RES [close_position]: {response}")
        logger.info(f"Position Closed: {symbol} via {side} MARKET for {quantity} (Order ID: {response.get('orderId')})")
        return True, response
    except BinanceAPIException as e:
        err_msg = f"Binance API Error closing pos: {e.message}"
        err_logger.error(err_msg)
        return False, {"error": err_msg}
    except Exception as e:
        err_msg = f"Unexpected Error closing pos: {str(e)}"
        err_logger.error(err_msg)
        return False, {"error": err_msg}

def get_listen_key() -> str:
    client = get_client()
    if is_mock():
        return "mock_listen_key"
    try:
        response = client.futures_stream_get_listen_key()
        return response
    except Exception as e:
        logger.error(f"Error fetching listen key: {e}")
        return ""
