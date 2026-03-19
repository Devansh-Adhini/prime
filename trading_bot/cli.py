import click
import sys
import json
from bot import get_client, place_order, setup_logging, get_market_price, get_balance, cancel_order, close_position
from bot.client import is_mock

# Setup logging once when CLI starts
setup_logging()

@click.group()
@click.option('--mock/--no-mock', default=False, help="Run in mock mode (no actual API calls).")
def cli(mock):
    """
    Simulated Trading Bot CLI for Binance Futures Testnet
    """
    # Initialize the client. This will set mock mode if true or if keys are missing.
    get_client(mock=mock)
    if is_mock():
        click.secho("[!] Running in MOCK mode.", fg="yellow")

@cli.command()
@click.option('--symbol', required=True, help='Trading pair symbol (e.g., BTCUSDT)')
def price(symbol):
    """Fetch the current market price for a symbol."""
    p = get_market_price(symbol)
    click.secho(f"Price for {symbol}: {p:.2f} USDT", fg="green")

@cli.command()
def balance():
    """Fetch the current USDT balance."""
    b = get_balance()
    click.secho(f"Balance: {b:.2f} USDT", fg="green")

@cli.command()
@click.option('--symbol', required=True, prompt=True, help='Trading pair symbol (e.g., BTCUSDT)')
@click.option('--side', required=True, prompt=True, type=click.Choice(['BUY', 'SELL'], case_sensitive=False))
@click.option('--type', 'order_type', required=True, prompt=True, type=click.Choice(['MARKET', 'LIMIT', 'STOP_MARKET'], case_sensitive=False))
@click.option('--quantity', required=True, prompt=True, type=float, help='Order quantity')
@click.option('--price', type=float, default=None, help='Required if order type is LIMIT')
def order(symbol, side, order_type, quantity, price):
    """Place a new order."""
    click.secho("\n--- Order Summary ---", fg="cyan")
    click.echo(f"Symbol:     {symbol.upper()}")
    click.echo(f"Side:       {side.upper()}")
    click.echo(f"Type:       {order_type.upper()}")
    click.echo(f"Quantity:   {quantity}")
    if price:
        click.echo(f"Price:      {price}")
    
    click.confirm("Do you want to proceed with this order?", abort=True)
    
    success, response = place_order(
        symbol=symbol,
        side=side,
        order_type=order_type,
        quantity=quantity,
        price=price
    )
    
    if success:
        click.secho("\n[SUCCESS] Order Placed Successfully!", fg="green", bold=True)
        # Safely extract formatting from success response
        o_id = response.get("orderId", "N/A")
        status = response.get("status", "N/A")
        executed = response.get("executedQty", "0")
        avg_price = response.get("avgPrice", "N/A")
        
        click.echo(f"Order ID:     {o_id}")
        click.echo(f"Status:       {status}")
        click.echo(f"Executed Qty: {executed}")
        click.echo(f"Avg Price:    {avg_price}")
        click.echo("\nRaw Response:")
        try:
            click.echo(json.dumps(response, indent=2))
        except:
            click.echo(response)
    else:
        click.secho("\n[FAILED] Order Placement Failed!", fg="red", bold=True)
        click.echo(response.get("error", "Unknown Error"))
        sys.exit(1)

@cli.command()
@click.option('--symbol', required=True, prompt=True, help='Trading pair symbol (e.g., BTCUSDT)')
@click.option('--order-id', required=True, prompt=True, type=int, help='Order ID to cancel')
def cancel(symbol, order_id):
    """Cancel an open order."""
    success, response = cancel_order(symbol, order_id)
    if success:
        click.secho(f"\n[SUCCESS] Order {order_id} Canceled Successfully!", fg="green", bold=True)
    else:
        click.secho(f"\n[FAILED] Order Cancellation Failed: {response.get('error')}", fg="red", bold=True)

@cli.command()
@click.option('--symbol', required=True, prompt=True, help='Trading pair symbol (e.g., BTCUSDT)')
def close(symbol):
    """Close an active position."""
    success, response = close_position(symbol)
    if success:
        click.secho(f"\n[SUCCESS] Position on {symbol} Closed Successfully!", fg="green", bold=True)
    else:
        click.secho(f"\n[FAILED] Position Closure Failed: {response.get('error')}", fg="red", bold=True)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        import shlex
        click.secho("=================================", fg="cyan", bold=True)
        click.secho(" Interactive Trading CLI Console", fg="cyan", bold=True)
        click.secho("=================================", fg="cyan", bold=True)
        click.echo("Type 'help' to see available commands (balance, price, order, cancel, close).")
        click.echo("Type 'exit' or 'quit' to exit.\n")
        
        while True:
            try:
                cmd = input("bot> ")
                if cmd.strip().lower() in ['exit', 'quit']:
                    break
                if not cmd.strip():
                    continue
                args = shlex.split(cmd)
                try:
                    # Execute command without killing the script on exit/failure
                    cli(args, standalone_mode=False)
                except click.exceptions.UsageError as e:
                    e.show()
                except click.exceptions.Exit:
                    pass
                except SystemExit:
                    pass
            except (KeyboardInterrupt, EOFError):
                break
    else:
        cli()
