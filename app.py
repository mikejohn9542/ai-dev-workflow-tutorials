import streamlit as st

from data import load_sales_data

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

st.write(f"Loaded {len(sales_df)} rows.")
