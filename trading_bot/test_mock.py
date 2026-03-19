import logging
from bot import get_client, place_order, setup_logging
from bot.client import is_mock

def run_tests():
    setup_logging()
    
    # Ensure client is initialized in mock mode since no API secret
    get_client()
    print(f"Is Mock Mode: {is_mock()}")
    
    print("\n--- Placing MARKET Order ---")
    success_market, res_market = place_order(
        symbol="BTCUSDT",
        side="BUY",
        order_type="MARKET",
        quantity=0.01
    )
    print(f"MARKET Success: {success_market}")
    
    print("\n--- Placing LIMIT Order ---")
    success_limit, res_limit = place_order(
        symbol="ETHUSDT",
        side="SELL",
        order_type="LIMIT",
        quantity=0.05,
        price=3500.0
    )
    print(f"LIMIT Success: {success_limit}")
    
    print("\nLogs should be generated in trading.log")

if __name__ == "__main__":
    run_tests()
