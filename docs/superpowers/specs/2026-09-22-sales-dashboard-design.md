# Design: E-Commerce Sales Dashboard

Source: [prd/ecommerce-analytics.md](../../../prd/ecommerce-analytics.md)
Tracked milestones: [TASKS.md](../../../TASKS.md) (TASK-1 through TASK-7)

## Overview

A single-page Streamlit dashboard reading `data/sales-data.csv` and showing
KPI cards, a monthly sales trend, and category/region breakdowns, per the
PRD's Phase 1 scope. One addition beyond the PRD: sidebar color pickers for
the two bar charts, requested during design.

## Architecture & file structure

```
app.py               Streamlit page: layout, sidebar, calls data.py + charts.py
data.py              Data loading (cached) and all calculations — no
                      Streamlit/Plotly imports, pure pandas
charts.py            Plotly figure builders — take a DataFrame + a color,
                      return a figure
tests/
  test_data.py       pytest tests for every function in data.py
requirements.txt     streamlit, pandas, plotly, pytest
venv/                Local virtual environment (gitignored)
data/sales-data.csv  Existing source data
```

`data.py` has no UI dependencies, so its calculations are testable without
running the app.

## Data flow & calculations

1. `load_sales_data(path)` — reads the CSV with pandas, parses `date` as
   datetime, validates the expected columns are present, returns a
   DataFrame. Wrapped in `@st.cache_data` so it only re-reads the file when
   the file changes, not on every sidebar interaction.
2. `total_sales(df)` — `df['total_amount'].sum()`.
3. `total_orders(df)` — `len(df)` (row count = transaction count).
4. `sales_by_month(df)` — group by `date.dt.to_period('M')`, sum
   `total_amount`, sorted chronologically. Feeds the trend chart.
5. `sales_by_category(df)` / `sales_by_region(df)` — group by
   category/region, sum `total_amount`, **sorted descending by value** (PRD
   requirement).
6. `app.py` loads the data once, then passes the DataFrame into each
   calculation function and each result into the matching chart builder.

## Error handling

- `load_sales_data()` raises `FileNotFoundError` (missing file) or
  `ValueError` (missing required columns) — plain Python exceptions, no
  Streamlit calls inside `data.py`.
- `app.py` wraps the load call in `try/except`. On failure it calls
  `st.error("Could not load data/sales-data.csv: <reason>")` and then
  `st.stop()`, so the user sees a clear message instead of a raw traceback
  and no charts attempt to render against missing data.

## Layout & sidebar

Top to bottom, matching the PRD's mockup:

1. Title: "ShopSmart Sales Dashboard"
2. Two KPI cards side by side (`st.columns(2)` + `st.metric()`): Total Sales
   (currency-formatted, e.g. `$116,500`) and Total Orders (comma-separated).
3. Sales trend line chart, full width, monthly granularity, interactive
   tooltips.
4. Category and region bar charts side by side (`st.columns(2)`), each
   sorted descending by sales value, interactive tooltips.

**Sidebar (addition beyond PRD Phase 1):** two `st.color_picker()` widgets —
"Category chart color" and "Region chart color" — each with a sensible
default. Changing either reruns the script and re-renders only that chart
in the new color; the cached data load keeps this fast.

## Testing strategy

- `tests/test_data.py` covers every function in `data.py` against a small,
  hand-built fixture DataFrame (not the full CSV) with known values, so
  expected results are hand-computable. Covers: sum/count correctness,
  monthly grouping and chronological ordering, category/region sums and
  descending sort order, and the missing-file/bad-column error paths.
- No automated tests for `charts.py` or `app.py`: Plotly/Streamlit
  rendering isn't meaningfully unit-testable. Consistent with testing only
  the data-transformation layer.

## Milestone mapping (informational — the plan does the detailed mapping)

- TASK-1 Environment setup — `venv/`, `requirements.txt`, project skeleton
- TASK-2 Data loading — `data.py` load + validation, its tests
- TASK-3 KPI cards — `total_sales`/`total_orders` + `app.py` metrics
- TASK-4 Sales trend chart — `sales_by_month` + `charts.py` trend builder
- TASK-5 Category/region breakdowns — remaining `data.py`/`charts.py`
  functions + sidebar color pickers
- TASK-6 Testing and refinement — full test suite pass, PRD acceptance
  criteria walkthrough
- TASK-7 Deployment — out of scope for the implementation plan; executed
  by the user from `main` after merge
