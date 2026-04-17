"""
main.py
-------
Entry point for the Stock Portfolio Tracker (CLI).

Responsibilities:
  - Bootstrap the application (print banner, initialise portfolio)
  - Run the main event loop
  - Route menu choices to business-logic functions in portfolio.py

Usage:
    python main.py
"""

import sys

import display
import portfolio as pf


def get_menu_choice() -> str:
    """
    Prompt the user for a menu selection and return the raw input.
    Validation is handled inside the main loop.
    """
    return input("\n  Enter your choice [1-8]: ").strip()


def run() -> None:
    """
    Main application loop.

    Keeps running until the user selects option 8 (Exit) or sends
    an EOF / keyboard-interrupt signal.
    """
    # -- Initialise in-memory portfolio ----------------------------
    # The portfolio is a plain dict: { "AAPL": 10, "TSLA": 5, ... }
    current_portfolio: pf.Portfolio = {}

    display.print_banner()
    display.info("Welcome! Use the menu below to manage your portfolio.")

    while True:
        display.print_menu()

        try:
            choice = get_menu_choice()
        except (EOFError, KeyboardInterrupt):
            # Graceful exit on Ctrl-C / Ctrl-Z
            print()
            display.info("Session ended by user. Goodbye!")
            sys.exit(0)

        # -- Route to the appropriate handler ----------------------
        if choice == "1":
            pf.add_stock(current_portfolio)

        elif choice == "2":
            pf.view_portfolio(current_portfolio)

        elif choice == "3":
            pf.calculate_total(current_portfolio)

        elif choice == "4":
            pf.save_to_csv(current_portfolio)

        elif choice == "5":
            pf.load_from_csv(current_portfolio)

        elif choice == "6":
            display.print_available_stocks()

        elif choice == "7":
            pf.remove_stock(current_portfolio)

        elif choice == "8":
            display.info("Thank you for using Stock Portfolio Tracker. Goodbye!")
            sys.exit(0)

        else:
            display.error(
                f"'{choice}' is not a valid option. "
                "Please enter a number between 1 and 8."
            )


# -- Script guard --------------------------------------------------
if __name__ == "__main__":
    run()
