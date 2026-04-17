"""
display.py
----------
Handles all console output formatting so that the rest of the
application stays clean and presentation-agnostic.

Functions here never mutate state -- they are pure display helpers.
"""

from stock_data import STOCK_PRICES, COMPANY_NAMES


# -- Column widths for the portfolio table --------------------------
_COL_SYMBOL  = 8
_COL_COMPANY = 28
_COL_PRICE   = 12
_COL_QTY     = 8
_COL_VALUE   = 14


def print_banner() -> None:
    """Print the application welcome banner."""
    banner = """
+============================================================+
|      [STOCK PORTFOLIO TRACKER]  v1.0  - CLI Edition        |
|             Python Standard Library Only                   |
+============================================================+
    """
    print(banner)


def print_menu() -> None:
    """Display the main menu options."""
    print("\n" + "-" * 46)
    print("  MAIN MENU")
    print("-" * 46)
    print("  [1]  Add / Update Stock")
    print("  [2]  View Portfolio")
    print("  [3]  Calculate Total Investment")
    print("  [4]  Save Portfolio to CSV")
    print("  [5]  Load Portfolio from CSV")
    print("  [6]  List Available Stocks")
    print("  [7]  Remove a Stock")
    print("  [8]  Exit")
    print("-" * 46)


def print_available_stocks() -> None:
    """Pretty-print all stocks available in the price dictionary."""
    print("\n" + "-" * 54)
    print(f"  {'SYMBOL':<{_COL_SYMBOL}} {'COMPANY':<{_COL_COMPANY}} {'PRICE (USD)':>{_COL_PRICE}}")
    print("-" * 54)
    for symbol, price in STOCK_PRICES.items():
        company = COMPANY_NAMES.get(symbol, "-")
        print(f"  {symbol:<{_COL_SYMBOL}} {company:<{_COL_COMPANY}} {price:>{_COL_PRICE},.2f}")
    print("-" * 54)


def print_portfolio(portfolio: dict) -> None:
    """
    Display the current portfolio in a formatted table.

    Args:
        portfolio: Mapping of stock symbol -> quantity owned.
    """
    if not portfolio:
        print("\n  [!]  Your portfolio is empty. Add stocks first.")
        return

    # Table header
    print()
    header = (
        f"  {'SYMBOL':<{_COL_SYMBOL}}"
        f"  {'COMPANY':<{_COL_COMPANY}}"
        f"  {'PRICE':>{_COL_PRICE}}"
        f"  {'QTY':>{_COL_QTY}}"
        f"  {'VALUE (USD)':>{_COL_VALUE}}"
    )
    separator = "-" * (len(header) - 2)   # -2 for leading spaces
    print("  " + separator)
    print(header)
    print("  " + separator)

    total_value: float = 0.0

    for symbol, qty in sorted(portfolio.items()):
        price   = STOCK_PRICES.get(symbol, 0.0)
        value   = price * qty
        company = COMPANY_NAMES.get(symbol, "-")
        total_value += value

        row = (
            f"  {symbol:<{_COL_SYMBOL}}"
            f"  {company:<{_COL_COMPANY}}"
            f"  {price:>{_COL_PRICE},.2f}"
            f"  {qty:>{_COL_QTY}}"
            f"  {value:>{_COL_VALUE},.2f}"
        )
        print(row)

    # Footer with total
    print("  " + separator)
    total_label = "TOTAL PORTFOLIO VALUE"
    print(f"  {total_label:<{_COL_SYMBOL + _COL_COMPANY + _COL_PRICE + 6}}"
          f"  {total_value:>{_COL_VALUE},.2f}")
    print("  " + separator)


def print_total(portfolio: dict) -> None:
    """
    Print only the grand-total investment value.

    Args:
        portfolio: Mapping of stock symbol -> quantity owned.
    """
    total: float = sum(
        STOCK_PRICES.get(sym, 0.0) * qty
        for sym, qty in portfolio.items()
    )
    print(f"\n  [$$]  Total Portfolio Value : USD {total:>14,.2f}")


def success(message: str) -> None:
    """Print a success confirmation message."""
    print(f"\n  [OK]  {message}")


def error(message: str) -> None:
    """Print an error message."""
    print(f"\n  [ERR] {message}")


def info(message: str) -> None:
    """Print a neutral informational message."""
    print(f"\n  [INF] {message}")
