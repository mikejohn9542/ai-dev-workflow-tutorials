# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Two things layered on top of each other:

1. **A tutorial** (`README.md`, `pre-work-setup.md`, `workshop-build-deploy.md`, `codex-companion.md`, `capstone-tools.md`) that teaches a PRD → `TASKS.md` → Superpowers brainstorming/writing-plans → build → deploy workflow.
2. **The tutorial's deliverable**: a Streamlit e-commerce sales dashboard, built by following that exact workflow. `prd/ecommerce-analytics.md` is the spec; `TASKS.md` is the milestone board; `docs/superpowers/specs/` and `docs/superpowers/plans/` hold the design doc and implementation plan Superpowers produced.

When asked to change the dashboard, treat `TASKS.md` and the PRD as the source of truth for requirements, not the markdown tutorial files.

## Commands

```bash
# Activate the virtual environment (Git Bash on Windows)
source venv/Scripts/activate

# Run the dashboard
streamlit run app.py

# Run the full test suite
pytest -v

# Run a single test
pytest tests/test_data.py::test_total_sales -v
```

`pytest.ini` sets `pythonpath = .`, so `data.py`/`charts.py` import cleanly from `tests/` without any package installation step.

## Architecture

Three modules, split strictly by what they're allowed to import — this boundary is intentional and load-bearing, not incidental:

- **`data.py`** — pure pandas. No Streamlit or Plotly import. `load_sales_data(path)` reads and validates `data/sales-data.csv` (required columns present, non-empty, `date` parses to datetime, `quantity`/`unit_price`/`total_amount` are numeric), raising `ValueError`/`FileNotFoundError` on failure. The rest of the module (`total_sales`, `total_orders`, `sales_by_month`, `sales_by_category`, `sales_by_region`) are calculations over the loaded DataFrame. Being import-free of the UI layer is what makes every one of these independently unit-testable in `tests/test_data.py`.
- **`charts.py`** — Plotly figure builders only (`build_trend_chart`, `build_category_chart`, `build_region_chart`). No Streamlit import. Category/region builders take a `color: str` parameter applied via `marker_color`, so chart color is driven by the caller, not hardcoded.
- **`app.py`** — the only file that imports `streamlit`. Wires `data.py` output into `charts.py` builders and into the page layout. Caching lives here (`@st.cache_data` wraps a thin `get_data()` call around `load_sales_data`), not in `data.py`, to keep the calculation layer free of Streamlit.

Keep new calculation logic in `data.py` and new chart types in `charts.py` — don't let Streamlit calls leak into either.

## Lessons

- A "testing and refinement" milestone must actually exercise the checks it claims to (e.g. watching terminal/browser output for warnings), not just confirm nothing crashes — the original TASK-6 pass reported no errors while `st.plotly_chart(..., use_container_width=True)` was actively emitting deprecation warnings that a real console check would have caught.
- Column-presence validation is not the same as data-quality validation. `load_sales_data` originally only checked that required columns existed; an empty CSV, an unparsed `date` column, or a non-numeric `total_amount` all passed that check and broke downstream code or silently produced wrong numbers. Validate dtypes and non-emptiness, not just column names.
- A test suite built entirely from a synthetic fixture (like `_sample_df()`) can pass even if the real data file no longer matches what the PRD promises. Keep at least one test that loads the actual source file (`data/sales-data.csv`) and asserts the documented expected values.

## Known gap

`load_sales_data`'s numeric-column validation catches genuinely non-numeric strings (e.g. `"abc"`) but not values pandas itself parses straight to `NaN` (e.g. a literal `"N/A"` in `total_amount`) — those pass the `is_numeric_dtype` check and would silently undercount a KPI with no error. This was found and deliberately left unfixed during the final branch review (documented in the PR); the real `data/sales-data.csv` is clean, so it isn't currently triggered.
