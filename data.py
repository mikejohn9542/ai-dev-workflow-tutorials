"""Data loading and calculations for the sales dashboard.

Pure pandas — no Streamlit or Plotly imports, so every function here
is testable without running the app.
"""
import pandas as pd

REQUIRED_COLUMNS = [
    "date", "order_id", "product", "category",
    "region", "quantity", "unit_price", "total_amount",
]


def load_sales_data(path: str) -> pd.DataFrame:
    """Load and validate the sales CSV at ``path``.

    Raises FileNotFoundError if the file doesn't exist (via pandas),
    and ValueError if any required column is missing.
    """
    df = pd.read_csv(path, parse_dates=["date"])

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    return df


def total_sales(df: pd.DataFrame) -> float:
    return df["total_amount"].sum()


def total_orders(df: pd.DataFrame) -> int:
    return len(df)
