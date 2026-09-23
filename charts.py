"""Plotly figure builders for the sales dashboard."""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def build_trend_chart(monthly_df: pd.DataFrame) -> go.Figure:
    fig = px.line(
        monthly_df,
        x="month",
        y="total_amount",
        markers=True,
        labels={"month": "Month", "total_amount": "Sales ($)"},
        title="Sales Trend Over Time",
    )
    fig.update_traces(hovertemplate="%{x}: $%{y:,.2f}<extra></extra>")
    return fig


def _build_bar_chart(
    df: pd.DataFrame, x_col: str, x_label: str, color: str, title: str
) -> go.Figure:
    fig = px.bar(
        df,
        x=x_col,
        y="total_amount",
        labels={x_col: x_label, "total_amount": "Sales ($)"},
        title=title,
    )
    fig.update_traces(marker_color=color, hovertemplate="%{x}: $%{y:,.2f}<extra></extra>")
    return fig


def build_category_chart(category_df: pd.DataFrame, color: str) -> go.Figure:
    return _build_bar_chart(category_df, "category", "Category", color, "Sales by Category")


def build_region_chart(region_df: pd.DataFrame, color: str) -> go.Figure:
    return _build_bar_chart(region_df, "region", "Region", color, "Sales by Region")
