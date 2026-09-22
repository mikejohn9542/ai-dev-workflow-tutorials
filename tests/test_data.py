import pandas as pd
import pytest

from data import load_sales_data, total_sales, total_orders

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


def _sample_df():
    return pd.DataFrame({
        "date": pd.to_datetime(["2024-01-05", "2024-01-20", "2024-02-10", "2024-02-15"]),
        "order_id": ["ORD-1", "ORD-2", "ORD-3", "ORD-4"],
        "product": ["A", "B", "C", "D"],
        "category": ["Electronics", "Audio", "Electronics", "Accessories"],
        "region": ["North", "South", "North", "East"],
        "quantity": [1, 2, 1, 3],
        "unit_price": [100.0, 50.0, 200.0, 10.0],
        "total_amount": [100.0, 100.0, 200.0, 30.0],
    })


def test_total_sales():
    assert total_sales(_sample_df()) == 430.0


def test_total_orders():
    assert total_orders(_sample_df()) == 4
