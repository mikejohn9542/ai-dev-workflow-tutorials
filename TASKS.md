# Tasks

This file tracks all work for the E-Commerce Analytics dashboard.

## Definition of Done

- Acceptance criteria for the milestone are met
- App runs locally with `streamlit run app.py`
- Changes are committed with the milestone ID in the commit message

## To Do

### TASK-7: Deployment to Streamlit Community Cloud
Deploy the finished dashboard to a public, shareable URL.
- [ ] App deployed successfully to Streamlit Community Cloud
- [ ] Public URL loads the dashboard without errors
- [ ] URL shared with stakeholders for review

Commit:

## In Progress

## Done

### TASK-1: Environment setup and project initialization
Set up the Python project structure and dependencies needed to build the dashboard.
- [x] Project folder structure created (e.g. app.py, data/, requirements.txt)
- [x] Dependencies installed (streamlit, pandas, plotly)
- [x] `streamlit run app.py` launches a blank/placeholder app with no errors

Commit: 908ca93

### TASK-2: Data loading and basic structure
Load sales-data.csv into a Pandas DataFrame and validate its structure.
- [x] CSV loads into a DataFrame without errors
- [x] Date, numeric, and categorical columns have correct types
- [x] Row count matches the source data (482 records)

Commit: fa825b3

### TASK-3: KPI cards implementation
Display Total Sales and Total Orders as KPI cards at the top of the dashboard.
- [x] Total Sales calculated correctly and formatted as currency (e.g. $116,500)
- [x] Total Orders calculated correctly with separator formatting
- [x] KPI cards render prominently on the dashboard

Commit: d4c4220

### TASK-4: Sales trend chart
Add a line chart showing sales over time.
- [x] Line chart shows sales trend with time on the X-axis and sales amount on the Y-axis
- [x] Interactive tooltips display exact values on hover
- [x] Chart renders within 2 seconds of data load

Commit: fc87f06

### TASK-5: Category and region breakdowns
Add bar charts showing sales by product category and by region.
- [x] Category bar chart shows all 5 categories, sorted by sales value (highest to lowest)
- [x] Region bar chart shows all 4 regions, sorted by sales value (highest to lowest)
- [x] Both charts have interactive tooltips with exact values

Commit: 0e91cb6

### TASK-6: Testing and refinement
Verify the dashboard meets all functional and non-functional requirements before deployment.
- [x] Dashboard loads within 5 seconds with no errors or warnings
- [x] All displayed values match expected calculations from the CSV
- [x] Dashboard has a professional appearance suitable for executive presentation

Note: the original TASK-6 pass found nothing wrong per its own (incomplete)
checks — it did not catch the deprecated `use_container_width` warnings, the
missing empty-CSV/bad-date/non-numeric validation, or the untested PRD
expected-output numbers. This fix wave is the real TASK-6 verification pass
and is what should have been caught the first time.

Commit: d484dc5
