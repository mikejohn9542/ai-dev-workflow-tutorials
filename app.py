import streamlit as st

from data import load_sales_data, total_sales, total_orders, sales_by_month
from charts import build_trend_chart

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

st.plotly_chart(build_trend_chart(sales_by_month(sales_df)), use_container_width=True)
