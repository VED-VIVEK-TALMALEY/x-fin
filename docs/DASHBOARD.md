# X-Fin Dashboard Guide

## Purpose

The Streamlit dashboard is the decision-support surface for X-Fin. It keeps the complete operating dataset visible while organizing it around the questions a practice leader needs to answer:

- Are we above or below plan?
- How much of the forecast is dependable?
- How much growth depends on pipeline conversion?
- Can delivery capacity support the plan?
- What should management do next?

The dashboard reads existing FastAPI endpoints through `dashboard/api.py`. It does not duplicate or replace backend calculations.

## Start the Dashboard

From the `x-fin` directory:

```powershell
.\venv\Scripts\python.exe -m streamlit run dashboard\app.py
```

The API must be running at `http://127.0.0.1:8000`. Streamlit normally opens at `http://localhost:8501`; if that port is busy, use the port shown by Streamlit.

## Page Model

### Decision Snapshot

The first section turns the intelligence payload into three leadership signals:

- **Forecast Confidence:** Monte Carlo probability of finishing at or above budget.
- **Revenue at Risk:** Weighted pipeline that is still dependent on conversion.
- **Delivery Signal:** Staffing-hours status and its data-quality caveat.

The leadership readout below these signals summarizes the positive position and the primary watchpoint in plain language.

### Executive Performance

This section shows actual revenue, budget variance, canonical forecast, committed backlog, pipeline, weighted pipeline, budget utilization, and gross margin. These are the core practice economics indicators.

### Executive Intelligence

This section presents qualitative and quantitative status together. The composite score is continuous; the qualitative risk labels are rule-based classifications of coverage and dependency.

### Forecast Decomposition

The metric row and waterfall chart show how the final forecast is constructed from committed backlog, weighted pipeline, utilization adjustment, and execution-risk adjustment.

### Forecast Risk and Revenue Quality

The risk-driver chart makes the forecast mix visible. Committed coverage and headroom are positive certainty signals; pipeline dependency is a dependency signal and should be read with its qualitative risk label.

The confidence distribution shows P10, P25, P50, P75, and P90 simulated outcomes against the budget line.

### Staffing and Capacity

Actual hours are compared with the hours budget. This is intentionally labeled as hours-versus-budget analysis. The current schema does not provide a true capacity-hours denominator, so the dashboard does not claim that hours attainment equals utilization.

### Insights and Recommended Actions

Insights are severity-coded findings from the API. Recommendations preserve their priority, rationale, and financial impact. These are management prompts, not automatic approvals or workflow assignments.

### Revenue, Forecast, Backlog, and Business Units

Charts provide trend and comparison views while the tables preserve the underlying detail:

- Monthly revenue trend
- Forecast variance
- Backlog position
- Business-unit revenue and margin
- Business-unit performance heatmap
- Historical forecast and budget accuracy

### Scenario Simulator

The existing scenario simulator sends user assumptions to `POST /scenarios/run`. It supports base revenue, pipeline revenue, utilization, pipeline conversion change, utilization change, billing-rate change, and project slippage. Results are shown as a comparison against the supplied baseline.

## Visual Language

The dashboard uses a dark charcoal presentation with restrained semantic colors:

- Cyan or blue: neutral forecast and operating information
- Green: favorable or committed position
- Amber: attention, uncertainty, or dependency
- Red: material risk or urgent review

Cards and charts are deliberately separated by whitespace. Tables remain available for auditability, while charts expose patterns faster than a dense metric wall.

## Hover Help

Section headings and important metrics expose hover help. Each explanation is written to answer:

1. What does this measure mean?
2. What data does it represent?
3. Why should a decision-maker care?

Plotly charts also provide point-level hover values.

## Data Availability Behavior

Every chart checks for missing or incomplete data and returns an empty chart or an informational message instead of failing the page. This matters for historical accuracy, business-unit fields, and staffing capacity fields that may not be populated in every environment.

## Design Principles

- Keep all material data accessible.
- Lead with decisions, not database fields.
- Distinguish forecast confidence from forecast upside.
- Do not call hours-versus-budget utilization without a capacity denominator.
- Keep narrative text short and traceable to API values.
- Preserve the backend as the single source of truth.
