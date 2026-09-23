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
    numeric column contains non-numeric or missing values.
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
        # A value pandas recognizes as an NA-like string (e.g. "N/A", "NULL",
        # "") is coerced straight to NaN during parsing, which still passes
        # is_numeric_dtype but silently undercounts sums like total_sales().
        if df[col].isna().any():
            raise ValueError(
                f"Column '{col}' contains missing or non-numeric values"
            )

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


def _sales_by(df: pd.DataFrame, column: str, dropna: bool = False) -> pd.DataFrame:
    """Sum ``total_amount`` grouped by ``column``, sorted descending.

    Rows with a null/NaN value in ``column`` are included by default under
    an "Unknown" label, so their sales aren't silently dropped from the
    total shown in the breakdown chart (pandas' groupby excludes NaN groups
    by default, which would otherwise make this total diverge from
    total_sales()). Pass ``dropna=True`` to exclude those rows instead.
    """
    if dropna:
        working = df.dropna(subset=[column])
    else:
        working = df.assign(**{column: df[column].fillna("Unknown")})

    return (
        working.groupby(column, as_index=False)["total_amount"]
        .sum()
        .sort_values("total_amount", ascending=False)
        .reset_index(drop=True)
    )


def sales_by_category(df: pd.DataFrame, dropna: bool = False) -> pd.DataFrame:
    return _sales_by(df, "category", dropna=dropna)


def sales_by_region(df: pd.DataFrame, dropna: bool = False) -> pd.DataFrame:
    return _sales_by(df, "region", dropna=dropna)
