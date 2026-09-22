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
