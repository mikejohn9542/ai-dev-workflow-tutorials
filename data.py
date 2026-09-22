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
    and ValueError if any required column is missing, the file has
    no data rows, the ``date`` column didn't parse as dates, or any
    numeric column contains non-numeric values.
    """
    df = pd.read_csv(path, parse_dates=["date"])

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    if len(df) == 0:
        raise ValueError("CSV file is empty")

    if not pd.api.types.is_datetime64_any_dtype(df["date"]):
        raise ValueError("Column 'date' could not be parsed as dates")

    for col in ("quantity", "unit_price", "total_amount"):
        if not pd.api.types.is_numeric_dtype(df[col]):
            raise ValueError(f"Column '{col}' must be numeric")

    return df


def total_sales(df: pd.DataFrame) -> float:
    return df["total_amount"].sum()


def total_orders(df: pd.DataFrame) -> int:
    return len(df)


def sales_by_month(df: pd.DataFrame) -> pd.DataFrame:
    monthly = (
        df.assign(month=df["date"].dt.to_period("M").astype(str))
        .groupby("month", as_index=False)["total_amount"]
        .sum()
        .sort_values("month")
        .reset_index(drop=True)
    )
    return monthly


def sales_by_category(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("category", as_index=False)["total_amount"]
        .sum()
        .sort_values("total_amount", ascending=False)
        .reset_index(drop=True)
    )


def sales_by_region(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("region", as_index=False)["total_amount"]
        .sum()
        .sort_values("total_amount", ascending=False)
        .reset_index(drop=True)
    )
