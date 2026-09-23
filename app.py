import streamlit as st

from data import (
    load_sales_data, total_sales, total_orders,
    sales_by_month, sales_by_category, sales_by_region,
)
from charts import build_trend_chart, build_category_chart, build_region_chart

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
st.title("ShopSmart Sales Dashboard")

DATA_PATH = "data/sales-data.csv"


@st.cache_data
def get_data(path: str):
    return load_sales_data(path)


try:
    sales_df = get_data(DATA_PATH)
except (FileNotFoundError, ValueError) as e:
    st.error(f"Could not load {DATA_PATH}: {e}")
    st.stop()

col1, col2 = st.columns(2)
col1.metric("Total Sales", f"${total_sales(sales_df):,.0f}")
col2.metric("Total Orders", f"{total_orders(sales_df):,}")

category_color = st.sidebar.color_picker("Category chart color", "#1f77b4")
region_color = st.sidebar.color_picker("Region chart color", "#2ca02c")

missing_category = int(sales_df["category"].isna().sum())
missing_region = int(sales_df["region"].isna().sum())
drop_missing_dims = False
if missing_category or missing_region:
    st.sidebar.info(
        f"{missing_category} row(s) have no category and {missing_region} "
        "row(s) have no region. They're included in the breakdown charts "
        "below under \"Unknown\" so totals still match the KPI cards."
    )
    drop_missing_dims = st.sidebar.checkbox(
        "Exclude rows without a category/region from the breakdown charts",
        value=False,
    )

st.plotly_chart(build_trend_chart(sales_by_month(sales_df)), width="stretch")

bar_col1, bar_col2 = st.columns(2)
bar_col1.plotly_chart(
    build_category_chart(
        sales_by_category(sales_df, dropna=drop_missing_dims), category_color
    ),
    width="stretch",
)
bar_col2.plotly_chart(
    build_region_chart(
        sales_by_region(sales_df, dropna=drop_missing_dims), region_color
    ),
    width="stretch",
)
