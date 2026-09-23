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


def build_category_chart(category_df: pd.DataFrame, color: str) -> go.Figure:
    fig = px.bar(
        category_df,
        x="category",
        y="total_amount",
        labels={"category": "Category", "total_amount": "Sales ($)"},
        title="Sales by Category",
    )
    fig.update_traces(marker_color=color, hovertemplate="%{x}: $%{y:,.2f}<extra></extra>")
    return fig


def build_region_chart(region_df: pd.DataFrame, color: str) -> go.Figure:
    fig = px.bar(
        region_df,
        x="region",
        y="total_amount",
        labels={"region": "Region", "total_amount": "Sales ($)"},
        title="Sales by Region",
    )
    fig.update_traces(marker_color=color, hovertemplate="%{x}: $%{y:,.2f}<extra></extra>")
    return fig
