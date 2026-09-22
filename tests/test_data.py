import pandas as pd
import pytest

from data import load_sales_data

REQUIRED_COLUMNS = [
    "date", "order_id", "product", "category",
    "region", "quantity", "unit_price", "total_amount",
]


def _write_csv(tmp_path, rows, columns=REQUIRED_COLUMNS):
    path = tmp_path / "sales.csv"
    df = pd.DataFrame(rows, columns=columns)
    df.to_csv(path, index=False)
    return str(path)


def test_load_sales_data_happy_path(tmp_path):
    rows = [
        ["2024-01-05", "ORD-1", "A", "Electronics", "North", 1, 100.0, 100.0],
        ["2024-01-20", "ORD-2", "B", "Audio", "South", 2, 50.0, 100.0],
    ]
    path = _write_csv(tmp_path, rows)

    df = load_sales_data(path)

    assert len(df) == 2
    assert list(df.columns) == REQUIRED_COLUMNS
    assert pd.api.types.is_datetime64_any_dtype(df["date"])


def test_load_sales_data_missing_file():
    with pytest.raises(FileNotFoundError):
        load_sales_data("does/not/exist.csv")


def test_load_sales_data_missing_column(tmp_path):
    columns = [c for c in REQUIRED_COLUMNS if c != "region"]
    rows = [["2024-01-05", "ORD-1", "A", "Electronics", 1, 100.0, 100.0]]
    path = _write_csv(tmp_path, rows, columns=columns)

    with pytest.raises(ValueError):
        load_sales_data(path)
