import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint
from Bot.client import get_client
from Bot.orders import place_order
from Bot.validators import validate_side, validate_order_type, validate_price, validate_stop_price
from Bot.logging_config import setup_logger

app = typer.Typer(help="Binance Futures Trading Bot CLI")
console = Console()
logger = setup_logger()

@app.command()
def trade(
    symbol: str = typer.Option(..., "--symbol", "-s", help="Symbol (e.g., BTCUSDT)"),
    side: str = typer.Option(..., "--side", "-d", help="Side (BUY/SELL)"),
    order_type: str = typer.Option(..., "--type", "-t", help="Order Type (MARKET/LIMIT/STOP_MARKET)"),
    quantity: float = typer.Option(..., "--qty", "-q", help="Quantity to trade"),
    price: float = typer.Option(None, "--price", "-p", help="Price (required for LIMIT)"),
    stop_price: float = typer.Option(None, "--stop", help="Stop Price (required for STOP_MARKET)")
):
    """
    Place an order on Binance Futures Testnet.
    """
    try:
        # Normalize and Validate input
        side = side.upper()
        order_type = order_type.upper()
        symbol = symbol.upper()

        validate_side(side)
        validate_order_type(order_type)
        validate_price(order_type, price)
        validate_stop_price(order_type, stop_price)

        with console.status("[bold green]Connecting to Binance Testnet...", spinner="dots"):
            client = get_client()

        # Print Order Summary
        summary_table = Table(title="📌 Order Request Summary", show_header=True, header_style="bold magenta")
        summary_table.add_column("Field", style="dim")
        summary_table.add_column("Value")
        summary_table.add_row("Symbol", symbol)
        summary_table.add_row("Side", f"[bold {'green' if side == 'BUY' else 'red'}]{side}[/]")
        summary_table.add_row("Type", order_type)
        summary_table.add_row("Quantity", str(quantity))
        if price: summary_table.add_row("Price", str(price))
        if stop_price: summary_table.add_row("Stop Price", str(stop_price))
        
        console.print(Panel(summary_table, expand=False, border_style="blue"))

        with console.status(f"[bold yellow]Placing {order_type} {side} order...", spinner="dots"):
            order = place_order(client, symbol, side, order_type, quantity, price, stop_price)

        # Success Output
        rprint("\n[bold green]✅ Order Placed Successfully![/bold green]")
        
        resp_table = Table(title="📄 Order Response Details", show_header=True, header_style="bold cyan")
        resp_table.add_column("Field", style="dim")
        resp_table.add_column("Value")
        resp_table.add_row("Order ID", str(order.get('orderId')))
        resp_table.add_row("Status", f"[bold]{order.get('status')}[/]")
        resp_table.add_row("Executed Qty", str(order.get('executedQty')))
        resp_table.add_row("Avg Price", str(order.get('avgPrice', 'N/A')))
        
        console.print(Panel(resp_table, expand=False, border_style="green"))

    except Exception as e:
        rprint(f"\n[bold red]❌ Error: {str(e)}[/bold red]")
        logger.error(f"CLI Error: {str(e)}")

if __name__ == "__main__":
    app()