"""
portfolio.py
------------
Core business-logic layer for the Stock Portfolio Tracker.

Each public function accepts / returns the `portfolio` dict
(symbol -> quantity) and never touches I/O directly -- all output
is delegated to display.py so this module stays testable.
"""

import csv
import os

from stock_data import STOCK_PRICES, DEFAULT_CSV_FILENAME
import display


# ------------------------------------------------------------------
# Type alias for clarity
# ------------------------------------------------------------------
Portfolio = dict   # { "AAPL": 10, "TSLA": 5, ... }


# ------------------------------------------------------------------
# 1. Add / Update Stock
# ------------------------------------------------------------------
def add_stock(portfolio: Portfolio) -> None:
    """
    Prompt the user for a stock symbol and quantity, then add it
    to the portfolio.  If the stock already exists, the quantity
    is updated (incremented) rather than overwritten.

    Handles:
        - Unknown stock symbols
        - Non-numeric quantity input
        - Negative or zero quantities
    """
    print("\n  -- Add / Update Stock --")

    raw_symbol = input("  Enter stock symbol (e.g. AAPL): ").strip().upper()

    if not raw_symbol:
        display.error("Stock symbol cannot be empty.")
        return

    if raw_symbol not in STOCK_PRICES:
        display.error(
            f"'{raw_symbol}' is not in our supported list. "
            "Use option [6] to see available stocks."
        )
        return

    raw_qty = input("  Enter quantity to add   : ").strip()

    try:
        quantity = int(raw_qty)
    except ValueError:
        display.error("Quantity must be a whole number (e.g. 10).")
        return

    if quantity <= 0:
        display.error("Quantity must be greater than zero.")
        return

    if raw_symbol in portfolio:
        # Stock already in portfolio -> update quantity
        old_qty = portfolio[raw_symbol]
        portfolio[raw_symbol] += quantity
        display.success(
            f"{raw_symbol} quantity updated: {old_qty} -> {portfolio[raw_symbol]}"
        )
    else:
        # New stock entry
        portfolio[raw_symbol] = quantity
        price = STOCK_PRICES[raw_symbol]
        display.success(
            f"{raw_symbol} added. Qty: {quantity}  |  "
            f"Value: USD {price * quantity:,.2f}"
        )


# ------------------------------------------------------------------
# 2. Remove a Stock
# ------------------------------------------------------------------
def remove_stock(portfolio: Portfolio) -> None:
    """
    Remove a stock entry entirely from the portfolio.

    Handles:
        - Empty portfolio
        - Stock not present in portfolio
    """
    if not portfolio:
        display.info("Portfolio is empty -- nothing to remove.")
        return

    print("\n  -- Remove Stock --")
    raw_symbol = input("  Enter stock symbol to remove: ").strip().upper()

    if not raw_symbol:
        display.error("Stock symbol cannot be empty.")
        return

    if raw_symbol not in portfolio:
        display.error(f"'{raw_symbol}' is not in your portfolio.")
        return

    confirm = input(
        f"  Remove {raw_symbol} (qty={portfolio[raw_symbol]})? [y/N]: "
    ).strip().lower()

    if confirm == "y":
        del portfolio[raw_symbol]
        display.success(f"{raw_symbol} removed from portfolio.")
    else:
        display.info("Removal cancelled.")


# ------------------------------------------------------------------
# 3. View Portfolio
# ------------------------------------------------------------------
def view_portfolio(portfolio: Portfolio) -> None:
    """Delegate portfolio display to the display module."""
    display.print_portfolio(portfolio)


# ------------------------------------------------------------------
# 4. Calculate Total Investment
# ------------------------------------------------------------------
def calculate_total(portfolio: Portfolio) -> None:
    """Print the grand-total investment value."""
    if not portfolio:
        display.info("Portfolio is empty -- add stocks first.")
        return
    display.print_total(portfolio)


# ------------------------------------------------------------------
# 5. Save Portfolio to CSV
# ------------------------------------------------------------------
def save_to_csv(portfolio: Portfolio) -> None:
    """
    Serialise the portfolio to a CSV file.

    The CSV format is:
        symbol,quantity,price_per_share,total_value

    The user is prompted for a filename; pressing Enter uses the
    default name defined in stock_data.py.

    Handles:
        - Empty portfolio (skips saving)
        - OS-level file write errors
    """
    if not portfolio:
        display.info("Portfolio is empty -- nothing to save.")
        return

    print("\n  -- Save to CSV --")
    filename = input(
        f"  Enter filename [default: {DEFAULT_CSV_FILENAME}]: "
    ).strip()

    if not filename:
        filename = DEFAULT_CSV_FILENAME

    # Ensure the filename ends with .csv
    if not filename.lower().endswith(".csv"):
        filename += ".csv"

    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            # Write header row
            writer.writerow(["Symbol", "Quantity", "Price_Per_Share", "Total_Value"])
            # Write each holding
            for symbol, qty in sorted(portfolio.items()):
                price = STOCK_PRICES.get(symbol, 0.0)
                value = price * qty
                writer.writerow([symbol, qty, f"{price:.2f}", f"{value:.2f}"])

        abs_path = os.path.abspath(filename)
        display.success(f"Portfolio saved to '{abs_path}'.")
    except OSError as exc:
        display.error(f"Could not write file: {exc}")


# ------------------------------------------------------------------
# 6. Load Portfolio from CSV
# ------------------------------------------------------------------
def load_from_csv(portfolio: Portfolio) -> None:
    """
    Load a previously saved portfolio from a CSV file.

    The function merges the file contents into the current
    in-memory portfolio (quantities are summed for duplicates).

    Handles:
        - File not found
        - Malformed rows (missing columns, bad numbers)
        - Unknown stock symbols in the file
    """
    print("\n  -- Load from CSV --")
    filename = input(
        f"  Enter filename [default: {DEFAULT_CSV_FILENAME}]: "
    ).strip()

    if not filename:
        filename = DEFAULT_CSV_FILENAME

    if not filename.lower().endswith(".csv"):
        filename += ".csv"

    if not os.path.isfile(filename):
        display.error(
            f"File '{filename}' not found. "
            "Make sure the file is in the correct directory."
        )
        return

    loaded_count = 0
    skipped_rows: list = []

    try:
        with open(filename, mode="r", newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)

            for line_num, row in enumerate(reader, start=2):   # +2: 1-header + 0-based
                symbol  = row.get("Symbol", "").strip().upper()
                raw_qty = row.get("Quantity", "").strip()

                # Validate symbol
                if symbol not in STOCK_PRICES:
                    skipped_rows.append(
                        f"Line {line_num}: unknown symbol '{symbol}'"
                    )
                    continue

                # Validate quantity
                try:
                    qty = int(raw_qty)
                    if qty <= 0:
                        raise ValueError("Non-positive quantity")
                except ValueError:
                    skipped_rows.append(
                        f"Line {line_num}: invalid quantity '{raw_qty}' for '{symbol}'"
                    )
                    continue

                # Merge into portfolio
                portfolio[symbol] = portfolio.get(symbol, 0) + qty
                loaded_count += 1

    except OSError as exc:
        display.error(f"Could not read file: {exc}")
        return

    # Summarise the load operation
    if loaded_count:
        display.success(
            f"Loaded {loaded_count} holding(s) from '{filename}'."
        )
    else:
        display.info("No valid holdings found in the file.")

    for warning in skipped_rows:
        display.info(f"Skipped -- {warning}")
