# Tasks

This file tracks all work for the E-Commerce Analytics dashboard.

## Definition of Done

- Acceptance criteria for the milestone are met
- App runs locally with `streamlit run app.py`
- Changes are committed with the milestone ID in the commit message

## To Do

### TASK-1: Environment setup and project initialization
Set up the Python project structure and dependencies needed to build the dashboard.
- [ ] Project folder structure created (e.g. app.py, data/, requirements.txt)
- [ ] Dependencies installed (streamlit, pandas, plotly)
- [ ] `streamlit run app.py` launches a blank/placeholder app with no errors

Commit:

### TASK-2: Data loading and basic structure
Load sales-data.csv into a Pandas DataFrame and validate its structure.
- [ ] CSV loads into a DataFrame without errors
- [ ] Date, numeric, and categorical columns have correct types
- [ ] Row count matches the source data (482 records)

Commit:

### TASK-3: KPI cards implementation
Display Total Sales and Total Orders as KPI cards at the top of the dashboard.
- [ ] Total Sales calculated correctly and formatted as currency (e.g. $116,500)
- [ ] Total Orders calculated correctly with separator formatting
- [ ] KPI cards render prominently on the dashboard

Commit:

### TASK-4: Sales trend chart
Add a line chart showing sales over time.
- [ ] Line chart shows sales trend with time on the X-axis and sales amount on the Y-axis
- [ ] Interactive tooltips display exact values on hover
- [ ] Chart renders within 2 seconds of data load

Commit:

### TASK-5: Category and region breakdowns
Add bar charts showing sales by product category and by region.
- [ ] Category bar chart shows all 5 categories, sorted by sales value (highest to lowest)
- [ ] Region bar chart shows all 4 regions, sorted by sales value (highest to lowest)
- [ ] Both charts have interactive tooltips with exact values

Commit:

### TASK-6: Testing and refinement
Verify the dashboard meets all functional and non-functional requirements before deployment.
- [ ] Dashboard loads within 5 seconds with no errors or warnings
- [ ] All displayed values match expected calculations from the CSV
- [ ] Dashboard has a professional appearance suitable for executive presentation

Commit:

### TASK-7: Deployment to Streamlit Community Cloud
Deploy the finished dashboard to a public, shareable URL.
- [ ] App deployed successfully to Streamlit Community Cloud
- [ ] Public URL loads the dashboard without errors
- [ ] URL shared with stakeholders for review

Commit:

## In Progress

## Done
