# Stock Portfolio Tracker 📈

A clean, modular **CLI-based Stock Portfolio Tracker** built entirely with
Python's standard library — no third-party packages required.

---

## Features

| Feature | Details |
|---|---|
| **Add / Update Stock** | Add a new stock or increment quantity if already held |
| **View Portfolio** | Formatted table with symbol, company, price, qty, value |
| **Total Investment** | Grand-total portfolio value at a glance |
| **Save to CSV** | Persist portfolio to a human-readable CSV file |
| **Load from CSV** | Restore / merge a previously saved portfolio |
| **List Available Stocks** | Browse all trackable tickers and prices |
| **Remove a Stock** | Delete a holding with a confirmation prompt |

---

## Project Structure

```
pf trkr/
├── main.py          # Entry point & event loop
├── portfolio.py     # All business logic (add, remove, save, load, total)
├── display.py       # All console formatting (pure output, no logic)
├── stock_data.py    # Predefined prices + constants
├── README.md        # GitHub-ready documentation
└── portfolio.csv    # Auto-generated on first save

```

---

## To Run

```bash
python main.py
```

> Requires **Python 3.10+** (uses `match` statement).  
> No pip installs needed — 100 % standard library.

---

## Supported Stocks

| Symbol | Company | Price (USD) |
|---|---|---|
| AAPL | Apple Inc. | 180.00 |
| TSLA | Tesla Inc. | 250.00 |
| GOOG | Alphabet (Google) | 2800.00 |
| AMZN | Amazon.com | 3300.00 |
| MSFT | Microsoft Corporation | 320.00 |
| META | Meta Platforms | 270.00 |
| NVDA | NVIDIA Corporation | 450.00 |
| NFLX | Netflix Inc. | 400.00 |
| AMD | Advanced Micro Devices | 105.00 |
| INTC | Intel Corporation | 35.00 |

---

## CSV Format

The saved CSV file follows this schema:

```
Symbol,Quantity,Price_Per_Share,Total_Value
AAPL,10,180.00,1800.00
TSLA,5,250.00,1250.00
```

---

## Design Principles

- **Separation of concerns** — `main.py` only routes; `portfolio.py` owns logic; `display.py` owns output.
- **No global state mutations** — the portfolio dict is passed explicitly to every function.
- **Defensive input handling** — every user input is validated before use.
- **Extensible price list** — add more tickers to `stock_data.py` without changing any other file.

---

## Author

