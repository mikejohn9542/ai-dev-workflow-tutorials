# Sales Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the ShopSmart e-commerce sales Streamlit dashboard (KPI cards, monthly trend chart, category/region breakdowns with customizable colors) from `data/sales-data.csv`.

**Architecture:** Three focused modules — `data.py` (pure pandas: loading + calculations, unit tested), `charts.py` (Plotly figure builders), `app.py` (Streamlit layout/sidebar, wires the two together). Caching and error handling live in `app.py` so `data.py` stays free of UI imports and fully testable.

**Tech Stack:** Python 3.11+, Streamlit, Pandas, Plotly (Express), pytest. Plain `venv/` virtual environment with `requirements.txt` (no uv/conda).

**Spec:** [docs/superpowers/specs/2026-09-22-sales-dashboard-design.md](../specs/2026-09-22-sales-dashboard-design.md)

## Global Constraints

- Work on the current feature branch (`feature/sales-dashboard`); do not create a git worktree.
- Dependencies via a plain `venv/` virtual environment and `requirements.txt` (no uv, no conda).
- All data calculations live in `data.py`, with pytest tests in `tests/test_data.py`. `data.py` imports only `pandas` — no `streamlit`, no `plotly`.
- Keep code simple and readable.
- Required CSV columns (from the PRD): `date, order_id, product, category, region, quantity, unit_price, total_amount`.
- Trend chart granularity: monthly.
- Category and region breakdowns: sorted descending by `total_amount`.
- On a missing file or missing required columns, the app shows `st.error(...)` and calls `st.stop()` — no raw traceback.
- CSV loading is cached via `@st.cache_data` so it only re-reads on file change, not on every sidebar interaction (implemented as a thin cached wrapper in `app.py` around `data.load_sales_data`, keeping `data.py` itself free of the `streamlit` import).
- Every commit message includes its milestone ID (TASK-1 .. TASK-7).
- TASK-7 (deployment) is executed by the user from `main` after merge — this plan stops before it.

---

### Task 1 (Milestone: TASK-1): Project scaffolding

**Files:**
- Create: `requirements.txt`
- Create: `app.py`
- Modify: none (`venv/` and `.pytest_cache/` etc. are already covered by `.gitignore`)

**Interfaces:**
- Produces: a runnable `app.py` with `st.set_page_config` and a title, which Task 2 will extend.

- [ ] **Step 1: Create the virtual environment**

Run:
```bash
python -m venv venv
```

- [ ] **Step 2: Activate it and confirm**

Run (Git Bash on Windows):
```bash
source venv/Scripts/activate
python --version
```
Expected: prints `(venv)` in the prompt and a Python 3.11+ version.

- [ ] **Step 3: Write `requirements.txt`**

```
streamlit>=1.38
pandas>=2.2
plotly>=5.24
pytest>=8.3
```

- [ ] **Step 4: Install dependencies**

Run:
```bash
pip install -r requirements.txt
```
Expected: installs without errors.

- [ ] **Step 5: Create `app.py` with a title-only skeleton**

```python
import streamlit as st

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
st.title("ShopSmart Sales Dashboard")
st.write("Dashboard content coming soon.")
```

- [ ] **Step 6: Run the app to confirm it starts**

Run:
```bash
streamlit run app.py
```
Expected: server starts, browser shows the title "ShopSmart Sales Dashboard" and the placeholder text, no errors in the terminal. Stop the server (Ctrl+C) once confirmed.

- [ ] **Step 7: Commit**

```bash
git add requirements.txt app.py
git commit -m "TASK-1: project scaffolding (venv, requirements, app skeleton)"
```

---

### Task 2 (Milestone: TASK-2): Data loading and validation

**Files:**
- Create: `data.py`
- Create: `tests/test_data.py`
- Modify: `app.py` (wire in cached loading + error handling)

**Interfaces:**
- Consumes: nothing from earlier tasks.
- Produces: `load_sales_data(path: str) -> pd.DataFrame`, raising `FileNotFoundError` on a missing file and `ValueError` on missing required columns. Later tasks (3, 4, 5) call this DataFrame's output.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_data.py`:

```python
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
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `pytest tests/test_data.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'data'` (or `ImportError`) since `data.py` doesn't exist yet.

- [ ] **Step 3: Write `data.py`**

```python
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
    and ValueError if any required column is missing.
    """
    df = pd.read_csv(path, parse_dates=["date"])

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    return df
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `pytest tests/test_data.py -v`
Expected: 3 passed.

- [ ] **Step 5: Wire loading into `app.py` with caching and error handling**

Replace the body of `app.py` with:

```python
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
```

- [ ] **Step 6: Run the app to confirm it loads real data**

Run:
```bash
streamlit run app.py
```
Expected: shows "Loaded 482 rows." with no errors. Stop the server once confirmed.

- [ ] **Step 7: Commit**

```bash
git add data.py tests/test_data.py app.py
git commit -m "TASK-2: data loading and validation"
```

---

### Task 3 (Milestone: TASK-3): KPI cards

**Files:**
- Modify: `data.py` (add `total_sales`, `total_orders`)
- Modify: `tests/test_data.py` (add tests for both)
- Modify: `app.py` (render the two KPI cards)

**Interfaces:**
- Consumes: `load_sales_data` output (a DataFrame with `total_amount`) from Task 2.
- Produces: `total_sales(df: pd.DataFrame) -> float`, `total_orders(df: pd.DataFrame) -> int`. No later task depends on these beyond `app.py` rendering.

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_data.py`:

```python
from data import total_sales, total_orders


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
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `pytest tests/test_data.py -v`
Expected: FAIL with `ImportError: cannot import name 'total_sales'`.

- [ ] **Step 3: Implement in `data.py`**

Append to `data.py`:

```python
def total_sales(df: pd.DataFrame) -> float:
    return df["total_amount"].sum()


def total_orders(df: pd.DataFrame) -> int:
    return len(df)
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `pytest tests/test_data.py -v`
Expected: all passed.

- [ ] **Step 5: Render KPI cards in `app.py`**

Add imports and a KPI section (after the try/except block, replacing the "Loaded N rows" line):

```python
from data import load_sales_data, total_sales, total_orders
```

```python
col1, col2 = st.columns(2)
col1.metric("Total Sales", f"${total_sales(sales_df):,.0f}")
col2.metric("Total Orders", f"{total_orders(sales_df):,}")
```

- [ ] **Step 6: Run the app and confirm the KPI values**

Run:
```bash
streamlit run app.py
```
Expected: Total Sales near `$116,500` and Total Orders `482`, matching the PRD's Expected Output table.

- [ ] **Step 7: Commit**

```bash
git add data.py tests/test_data.py app.py
git commit -m "TASK-3: KPI cards (total sales, total orders)"
```

---

### Task 4 (Milestone: TASK-4): Sales trend chart

**Files:**
- Modify: `data.py` (add `sales_by_month`)
- Modify: `tests/test_data.py` (add test for it)
- Create: `charts.py` (add `build_trend_chart`)
- Modify: `app.py` (render the trend chart)

**Interfaces:**
- Consumes: `load_sales_data` output from Task 2.
- Produces: `sales_by_month(df: pd.DataFrame) -> pd.DataFrame` with columns `["month", "total_amount"]`, `month` as a string label (e.g. `"2024-01"`), sorted chronologically ascending. `build_trend_chart(monthly_df: pd.DataFrame) -> plotly.graph_objects.Figure` in `charts.py`, consumed only by `app.py`.

- [ ] **Step 1: Write the failing test**

Append to `tests/test_data.py`:

```python
from data import sales_by_month


def test_sales_by_month():
    result = sales_by_month(_sample_df())

    assert list(result["month"]) == ["2024-01", "2024-02"]
    assert list(result["total_amount"]) == [200.0, 230.0]
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `pytest tests/test_data.py -v`
Expected: FAIL with `ImportError: cannot import name 'sales_by_month'`.

- [ ] **Step 3: Implement in `data.py`**

Append to `data.py`:

```python
def sales_by_month(df: pd.DataFrame) -> pd.DataFrame:
    monthly = (
        df.assign(month=df["date"].dt.to_period("M").astype(str))
        .groupby("month", as_index=False)["total_amount"]
        .sum()
        .sort_values("month")
        .reset_index(drop=True)
    )
    return monthly
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `pytest tests/test_data.py -v`
Expected: all passed.

- [ ] **Step 5: Create `charts.py` with the trend chart builder**

```python
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
```

- [ ] **Step 6: Render the chart in `app.py`**

Add the import and section (after the KPI columns):

```python
from data import load_sales_data, total_sales, total_orders, sales_by_month
from charts import build_trend_chart
```

```python
st.plotly_chart(build_trend_chart(sales_by_month(sales_df)), use_container_width=True)
```

- [ ] **Step 7: Run the app and confirm the chart renders**

Run:
```bash
streamlit run app.py
```
Expected: a line chart with 12 monthly points below the KPI cards, tooltips show exact dollar values on hover.

- [ ] **Step 8: Commit**

```bash
git add data.py tests/test_data.py charts.py app.py
git commit -m "TASK-4: sales trend chart"
```

---

### Task 5 (Milestone: TASK-5): Category and region breakdowns with sidebar colors

**Files:**
- Modify: `data.py` (add `sales_by_category`, `sales_by_region`)
- Modify: `tests/test_data.py` (add tests for both, including sort order)
- Modify: `charts.py` (add `build_category_chart`, `build_region_chart`)
- Modify: `app.py` (sidebar color pickers, two-column bar chart layout)

**Interfaces:**
- Consumes: `load_sales_data` output from Task 2.
- Produces: `sales_by_category(df) -> pd.DataFrame` and `sales_by_region(df) -> pd.DataFrame`, both with columns `["category"|"region", "total_amount"]`, sorted descending by `total_amount`. `build_category_chart(df, color: str) -> go.Figure` and `build_region_chart(df, color: str) -> go.Figure` in `charts.py`, consumed only by `app.py`.

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_data.py`:

```python
from data import sales_by_category, sales_by_region


def test_sales_by_category_sorted_descending():
    result = sales_by_category(_sample_df())

    assert list(result["category"]) == ["Electronics", "Audio", "Accessories"]
    assert list(result["total_amount"]) == [300.0, 100.0, 30.0]


def test_sales_by_region_sorted_descending():
    result = sales_by_region(_sample_df())

    assert list(result["region"]) == ["North", "South", "East"]
    assert list(result["total_amount"]) == [300.0, 100.0, 30.0]
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `pytest tests/test_data.py -v`
Expected: FAIL with `ImportError: cannot import name 'sales_by_category'`.

- [ ] **Step 3: Implement in `data.py`**

Append to `data.py`:

```python
def sales_by_category(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("category", as_index=False)["total_amount"]
        .sum()
        .sort_values("total_amount", ascending=False)
        .reset_index(drop=True)
    )


def sales_by_region(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("region", as_index=False)["total_amount"]
        .sum()
        .sort_values("total_amount", ascending=False)
        .reset_index(drop=True)
    )
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `pytest tests/test_data.py -v`
Expected: all passed.

- [ ] **Step 5: Add chart builders to `charts.py`**

Append to `charts.py`:

```python
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
```

- [ ] **Step 6: Add sidebar color pickers and render both charts in `app.py`**

Add the import:

```python
from data import (
    load_sales_data, total_sales, total_orders,
    sales_by_month, sales_by_category, sales_by_region,
)
from charts import build_trend_chart, build_category_chart, build_region_chart
```

Add the sidebar (before or after the KPI section — placement in the file doesn't matter since Streamlit renders the sidebar separately):

```python
category_color = st.sidebar.color_picker("Category chart color", "#1f77b4")
region_color = st.sidebar.color_picker("Region chart color", "#2ca02c")
```

Add the two-column chart section (after the trend chart):

```python
bar_col1, bar_col2 = st.columns(2)
bar_col1.plotly_chart(
    build_category_chart(sales_by_category(sales_df), category_color),
    use_container_width=True,
)
bar_col2.plotly_chart(
    build_region_chart(sales_by_region(sales_df), region_color),
    use_container_width=True,
)
```

- [ ] **Step 7: Run the app and confirm both charts and the color pickers work**

Run:
```bash
streamlit run app.py
```
Expected: category and region bar charts side by side, both sorted highest-to-lowest, with a sidebar showing two color pickers. Changing a color picker updates the matching chart.

- [ ] **Step 8: Commit**

```bash
git add data.py tests/test_data.py charts.py app.py
git commit -m "TASK-5: category and region breakdowns with sidebar colors"
```

---

### Task 6 (Milestone: TASK-6): Testing and refinement

**Files:**
- Modify: none expected (fixes only if a check below fails)

**Interfaces:**
- Consumes: the full app and test suite from Tasks 1-5.
- Produces: nothing new — this task is a verification pass.

- [ ] **Step 1: Run the full test suite**

Run:
```bash
pytest -v
```
Expected: all tests pass (should be 3 + 2 + 1 + 2 = 8 tests across `test_data.py`).

- [ ] **Step 2: Run the app fresh and check for warnings**

Run:
```bash
streamlit run app.py
```
Expected: no errors or warnings printed in the terminal, page loads in well under 5 seconds.

- [ ] **Step 3: Walk the PRD's Acceptance Criteria against the running app**

Open `prd/ecommerce-analytics.md`'s Acceptance Criteria section side by side with the browser tab and confirm each item by eye:
- KPIs visible (Total Sales ~$116,500, Total Orders 482)
- Trend chart shows 12 months, correct shape
- Category chart sorted descending, all 5 categories shown
- Region chart sorted descending, all 4 regions shown
- No errors/warnings anywhere in the terminal or browser console
- Overall look is clean enough for an executive audience

If any item fails, fix the specific file (`data.py`, `charts.py`, or `app.py`) and re-run steps 1-3 until all pass.

- [ ] **Step 4: Commit any fixes (skip if none were needed)**

```bash
git add -A
git commit -m "TASK-6: testing and refinement"
```

---

## TASK-7: Deployment — executed by you, not this plan

This plan stops here. Deployment to Streamlit Community Cloud requires your GitHub and Streamlit accounts and a go/no-go call that's yours to make, not the agent's. After this branch is reviewed and merged to `main` (outside this plan), deploy it yourself:

1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
2. Click **New app**, select your repository, branch `main`, and main file path `app.py`.
3. Click **Deploy**. Streamlit Cloud installs from `requirements.txt` and starts the app.
4. Confirm the public URL loads the dashboard correctly, then share it with stakeholders per the PRD.
