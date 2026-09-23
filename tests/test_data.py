import pandas as pd
import pytest

from data import (
    load_sales_data, total_sales, total_orders, sales_by_month,
    sales_by_category, sales_by_region,
)

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


def test_load_sales_data_empty_csv(tmp_path):
    path = _write_csv(tmp_path, [])

    with pytest.raises(ValueError):
        load_sales_data(path)


def test_load_sales_data_unparseable_date(tmp_path):
    rows = [["not-a-date", "ORD-1", "A", "Electronics", "North", 1, 100.0, 100.0]]
    path = _write_csv(tmp_path, rows)

    with pytest.raises(ValueError):
        load_sales_data(path)


def test_load_sales_data_non_numeric_total_amount(tmp_path):
    rows = [["2024-01-05", "ORD-1", "A", "Electronics", "North", 1, 100.0, "invalid"]]
    path = _write_csv(tmp_path, rows)

    with pytest.raises(ValueError):
        load_sales_data(path)


def test_load_sales_data_na_like_string_in_numeric_column(tmp_path):
    # "N/A" is silently parsed straight to NaN by pandas (it's in the
    # default na_values list), so it stays numeric dtype and would
    # otherwise sneak past an is_numeric_dtype-only check.
    rows = [
        ["2024-01-05", "ORD-1", "A", "Electronics", "North", 1, 100.0, 100.0],
        ["2024-01-06", "ORD-2", "B", "Electronics", "North", 1, 100.0, "N/A"],
    ]
    path = _write_csv(tmp_path, rows)

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


def test_sales_by_month():
    result = sales_by_month(_sample_df())

    assert list(result["month"]) == ["2024-01", "2024-02"]
    assert list(result["total_amount"]) == [200.0, 230.0]


def test_sales_by_category_sorted_descending():
    result = sales_by_category(_sample_df())

    assert list(result["category"]) == ["Electronics", "Audio", "Accessories"]
    assert list(result["total_amount"]) == [300.0, 100.0, 30.0]


def test_sales_by_region_sorted_descending():
    result = sales_by_region(_sample_df())

    assert list(result["region"]) == ["North", "South", "East"]
    assert list(result["total_amount"]) == [300.0, 100.0, 30.0]


def _sample_df_with_missing_dims():
    df = _sample_df()
    df.loc[1, "category"] = None
    df.loc[2, "region"] = None
    return df


def test_sales_by_category_includes_missing_as_unknown_by_default():
    df = _sample_df_with_missing_dims()

    result = sales_by_category(df)

    # Nothing is dropped: every row's total_amount is still represented.
    assert result["total_amount"].sum() == total_sales(df)
    assert "Unknown" in list(result["category"])


def test_sales_by_category_dropna_excludes_missing():
    df = _sample_df_with_missing_dims()

    result = sales_by_category(df, dropna=True)

    assert "Unknown" not in list(result["category"])
    assert result["total_amount"].sum() < total_sales(df)


def test_sales_by_region_includes_missing_as_unknown_by_default():
    df = _sample_df_with_missing_dims()

    result = sales_by_region(df)

    assert result["total_amount"].sum() == total_sales(df)
    assert "Unknown" in list(result["region"])


def test_sales_by_region_dropna_excludes_missing():
    df = _sample_df_with_missing_dims()

    result = sales_by_region(df, dropna=True)

    assert "Unknown" not in list(result["region"])
    assert result["total_amount"].sum() < total_sales(df)


def test_real_csv_matches_prd_expected_output():
    df = load_sales_data("data/sales-data.csv")

    assert total_orders(df) == 482
    assert round(total_sales(df)) == 116500
    assert len(sales_by_category(df)) == 5
    assert len(sales_by_region(df)) == 4
    assert len(sales_by_month(df)) == 12
