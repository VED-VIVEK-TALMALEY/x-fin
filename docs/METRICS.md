# X-Fin Dashboard Metrics

This document defines the metrics shown in the Streamlit dashboard. Values are supplied by the FastAPI intelligence and analytics endpoints unless explicitly described as presentation-only.

## Revenue and Plan

| Metric | Definition | Decision use |
|---|---|---|
| Actual Revenue | Recognized revenue delivered to date. | Measures realized performance. |
| Budget Revenue | Approved revenue target for the reporting period. | Baseline for plan comparison. |
| Budget Gap | Actual revenue minus budget revenue. | Shows absolute upside or shortfall. |
| Budget Gap % | Budget gap divided by budget revenue, expressed as a percentage. | Normalizes performance across periods. |
| Forecast Revenue | Canonical risk-adjusted revenue forecast. | Primary forward-looking operating number. |
| Forecast Gap | Forecast revenue minus budget revenue. | Shows expected upside or shortfall. |
| Forecast Gap % | Forecast gap divided by budget revenue. | Compares forecast position with plan. |
| Gross Margin | Actual revenue minus actual direct cost. | Shows contribution before other operating costs. |
| Gross Margin % | Gross margin divided by actual revenue. | Compares profitability quality. |

## Coverage and Risk

| Metric | Definition | Decision use |
|---|---|---|
| Committed Backlog | Pipeline value in committed delivery or closed-won stages. | Indicates revenue with stronger delivery certainty. |
| Weighted Pipeline | Pipeline value multiplied by opportunity probability. | Estimates likely pipeline contribution. |
| Forward Revenue | Committed backlog plus weighted pipeline. | Shows the forward revenue base. |
| Forward Coverage | Forward revenue divided by budget revenue. | Indicates whether the forward position covers plan. |
| Committed Coverage | Committed backlog divided by forecast revenue. | Indicates how much forecast is already supported. |
| Pipeline Dependency | Weighted pipeline divided by forward revenue. | Shows reliance on future conversion. |
| Forecast Headroom | Forecast revenue minus budget revenue. | Shows the absolute cushion above or below plan. |
| Risk Score | Composite quantitative risk score from coverage and dependency signals. | Provides a continuous comparison measure. |
| Overall Risk | Qualitative classification from the intelligence rules. | Communicates the management attention level. |

## Forecast Distribution

The Monte Carlo section uses deterministic inputs and a fixed seed from the API response.

- **P10:** Lower-bound simulated outcome; only 10% of outcomes are lower.
- **P50:** Median simulated outcome.
- **P90:** Upper-bound simulated outcome; only 10% of outcomes are higher.
- **Probability above budget:** Share of simulations at or above budget.
- **Probability below budget:** Share of simulations below budget.
- **Range P10-P90:** Width of the central forecast outcome range.

A high probability of exceeding budget does not eliminate execution risk when the forecast depends heavily on uncommitted pipeline.

## Staffing and Capacity

| Metric | Definition | Limitation |
|---|---|---|
| Actual Hours | Delivery hours recorded in actuals. | Reflects recorded work, not available capacity. |
| Hours Budget | Planned delivery hours. | A planning baseline, not a capacity denominator. |
| Hours vs Budget | Actual hours relative to hours budget. | Must not be described as utilization without capacity hours. |
| Blended Cost / Hour | Actual cost divided by actual hours. | Sensitive to labor mix and data completeness. |
| Capacity Status | Rule-based status from staffing hours and data-quality checks. | Requires review when the capacity denominator is absent. |

## Business Unit Views

Business-unit charts use the fields available from the analytics endpoint:

- Actual revenue
- Budget revenue
- Variance
- Variance percentage
- Gross margin percentage

The heatmap is a comparison view, not a new calculation layer. It helps identify concentration, margin differences, and outlier performance quickly.

## Decision Snapshot Logic

The dashboard's decision snapshot is presentation logic built from existing API values:

- **Forecast Confidence** uses Monte Carlo probability above budget.
- **Revenue at Risk** surfaces weighted pipeline because it depends on conversion.
- **Delivery Signal** surfaces the staffing capacity status and its data-quality note.

The snapshot is intentionally not a new backend forecast. It is a concise interpretation of the existing canonical payload.

## Data Quality Rules

- Missing numeric values display as zero or an unavailable state according to the existing formatter.
- Missing arrays produce an informational empty state.
- Staffing utilization, bench, and capacity economics are not treated as authoritative when the capacity-hours denominator is missing.
- The dashboard does not recompute the canonical forecast from raw analytics endpoints.
- Financial values are displayed in Indian rupee notation using K, M, or B abbreviations where appropriate.
