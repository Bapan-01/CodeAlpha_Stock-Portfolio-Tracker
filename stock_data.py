"""
stock_data.py
-------------
Stores the predefined stock-price dictionary and any static
reference data used across the application.

All prices are in USD and represent fictionalised demo values
suitable for an internship/demo project.
"""

# ------------------------------------------------------------------
# Predefined stock prices  (symbol -> price per share in USD)
# ------------------------------------------------------------------
STOCK_PRICES: dict = {
    "AAPL":  180.00,   # Apple Inc.
    "TSLA":  250.00,   # Tesla Inc.
    "GOOG": 2800.00,   # Alphabet (Google)
    "AMZN": 3300.00,   # Amazon.com
    "MSFT":  320.00,   # Microsoft Corporation
    "META":  270.00,   # Meta Platforms
    "NVDA":  450.00,   # NVIDIA Corporation
    "NFLX":  400.00,   # Netflix Inc.
    "AMD":   105.00,   # Advanced Micro Devices
    "INTC":   35.00,   # Intel Corporation
}

# Human-readable company names mapped to ticker symbols
COMPANY_NAMES: dict = {
    "AAPL":  "Apple Inc.",
    "TSLA":  "Tesla Inc.",
    "GOOG":  "Alphabet (Google)",
    "AMZN":  "Amazon.com",
    "MSFT":  "Microsoft Corporation",
    "META":  "Meta Platforms",
    "NVDA":  "NVIDIA Corporation",
    "NFLX":  "Netflix Inc.",
    "AMD":   "Advanced Micro Devices",
    "INTC":  "Intel Corporation",
}

# Default CSV file name used for save / load operations
DEFAULT_CSV_FILENAME: str = "portfolio.csv"
