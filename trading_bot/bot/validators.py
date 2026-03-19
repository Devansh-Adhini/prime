def validate_symbol(symbol: str) -> str:
    symbol = symbol.upper().strip()
    if not symbol:
        raise ValueError("Symbol cannot be empty.")
    if not symbol.endswith("USDT"):
        raise ValueError("Symbol must end with USDT for USDT-M futures (e.g., BTCUSDT).")
    return symbol

def validate_side(side: str) -> str:
    side = side.upper().strip()
    if side not in ["BUY", "SELL"]:
        raise ValueError("Side must be either BUY or SELL.")
    return side

def validate_order_type(order_type: str) -> str:
    order_type = order_type.upper().strip()
    if order_type not in ["MARKET", "LIMIT", "STOP_MARKET", "STOP"]:
        raise ValueError("Order type must be MARKET, LIMIT, or a supported STOP variant.")
    return order_type

def validate_quantity(quantity: float) -> float:
    try:
        qty = float(quantity)
    except (TypeError, ValueError):
        raise ValueError("Quantity must be a valid number.")
    if qty <= 0:
        raise ValueError("Quantity must be greater than 0.")
    return qty

def validate_price(price: float, order_type: str) -> float:
    if order_type == "LIMIT":
        try:
            p = float(price)
        except (TypeError, ValueError):
            raise ValueError("Price is required and must be a valid number for LIMIT orders.")
        if p <= 0:
            raise ValueError("Price must be greater than 0.")
        return p
    return 0.0
