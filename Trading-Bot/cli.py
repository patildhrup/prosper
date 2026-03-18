import typer
import questionary
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint
from Bot.client import get_client
from Bot.orders import place_order, get_futures_balance
from Bot.validators import validate_side, validate_order_type, validate_price, validate_stop_price
from Bot.logging_config import setup_logger

app = typer.Typer(help="Binance Futures Trading Bot CLI")
console = Console()
logger = setup_logger()

def interactive_mode():
    """
    User-friendly interactive mode that loops until exit.
    """
    rprint(Panel("[bold cyan]Welcome to Binance Futures Trading Bot[/bold cyan]\n[dim]Interactive Mode - Press Ctrl+C to exit any time[/dim]", expand=False))
    
    with console.status("[bold green]Connecting to Binance Testnet...", spinner="dots"):
        try:
            client = get_client()
        except Exception as e:
            rprint(f"[bold red]Failed to connect: {str(e)}[/bold red]")
            return

    while True:
        action = questionary.select(
            "What would you like to do?",
            choices=[
                "Place a New Order",
                "Check Balance",
                "Exit"
            ]
        ).ask()

        if action == "Exit" or action is None:
            rprint("[yellow]Goodbye![/yellow]")
            break

        if action == "Check Balance":
            with console.status("[bold cyan]Fetching Balance...", spinner="dots"):
                try:
                    balance = get_futures_balance(client)
                    if balance:
                        rprint(Panel(
                            f"[bold cyan]USDT Balance:[/bold cyan] [green]{balance['balance']} USDT[/green]\n"
                            f"[bold dim]Available Balance:[/bold dim] {balance['availableBalance']} USDT",
                            title="💰 Account Balance",
                            expand=False
                        ))
                    else:
                        rprint("[yellow]USDT balance not found.[/yellow]")
                except Exception as e:
                    rprint(f"[bold red]Error fetching balance: {str(e)}[/bold red]")

        if action == "Place a New Order":
            try:
                symbol = questionary.text("Enter Symbol (e.g., BTCUSDT):", default="BTCUSDT").ask()
                if not symbol: continue

                side = questionary.select(
                    "Select Side:",
                    choices=["BUY", "SELL"]
                ).ask()

                order_type = questionary.select(
                    "Select Order Type:",
                    choices=["MARKET", "LIMIT", "STOP_MARKET"]
                ).ask()

                quantity = float(questionary.text("Enter Quantity:", default="0.1").ask())
                
                price = None
                if order_type == "LIMIT":
                    price = float(questionary.text("Enter Limit Price:").ask())
                
                stop_price = None
                if order_type == "STOP_MARKET":
                    stop_price = float(questionary.text("Enter Stop Price:").ask())

                # Reuse the trade logic
                run_trade(symbol, side, order_type, quantity, price, stop_price, client)

            except Exception as e:
                rprint(f"[bold red]Invalid Input: {str(e)}[/bold red]")

def run_trade(symbol, side, order_type, quantity, price, stop_price, client=None):
    """
    Core trade execution logic shared between CLI and Interactive mode.
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

        if not client:
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
        logger.error(f"Execution Error: {str(e)}")

@app.command()
def trade(
    symbol: str = typer.Option(None, "--symbol", "-s", help="Symbol (e.g., BTCUSDT)"),
    side: str = typer.Option(None, "--side", "-d", help="Side (BUY/SELL)"),
    order_type: str = typer.Option(None, "--type", "-t", help="Order Type (MARKET/LIMIT/STOP_MARKET)"),
    quantity: float = typer.Option(None, "--qty", "-q", help="Quantity to trade"),
    price: float = typer.Option(None, "--price", "-p", help="Price (required for LIMIT)"),
    stop_price: float = typer.Option(None, "--stop", help="Stop Price (required for STOP_MARKET)"),
    interactive: bool = typer.Option(True, "--interactive/--no-interactive", help="Run in interactive mode")
):
    """
    Place an order on Binance Futures Testnet.
    Defaults to interactive mode if no arguments are provided.
    """
    # If any core argument is provided, run as one-off command
    if symbol or side or order_type or quantity:
        run_trade(symbol, side, order_type, quantity, price, stop_price)
    else:
        # Otherwise run interactive mode
        interactive_mode()

if __name__ == "__main__":
    app()