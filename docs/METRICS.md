# X-Fin Financial Telemetry & Metrics Specification

> **Audience:** Practice Finance Officers, Engagement Directors, Technical Leads

---

## Financial Metric Taxonomy & Relationships

```mermaid
graph TD
    subgraph RevenuePillar["1. REVENUE & FINANCIAL ACTUALS"]
        M_ACT["<b>Actual Revenue ($R_{\text{act}}$)</b><br/>$\sum \text{actual\_revenue}$"]
        M_BDG["<b>Budget Target ($R_{\text{bdg}}$)</b><br/>$\sum \text{revenue\_budget}$"]
        M_GAP["<b>Budget Gap ($\Delta_{\text{bdg}}$)</b><br/>$R_{\text{act}} - R_{\text{bdg}}$"]
        M_GM["<b>Gross Margin ($GM$)</b><br/>$R_{\text{act}} - \text{Cost}_{\text{act}}$"]
        M_GMP["<b>Gross Margin % ($GM_{\%}$)</b><br/>$(GM / R_{\text{act}}) \times 100$"]

        M_ACT & M_BDG --> M_GAP
        M_ACT --> M_GM --> M_GMP
    end

    subgraph ForecastPillar["2. DELIVERABLE FORECAST & HAIRCUTS"]
        M_CB["<b>Committed Backlog ($B_{\text{comm}}$)</b><br/>Signed SOWs & In Delivery"]
        M_WP["<b>Weighted Pipeline ($P_{\text{wt}}$)</b><br/>$\sum (\text{Value} \times \text{Prob})$"]
        M_UA["<b>Util Adjustment ($A_{\text{util}}$)</b><br/>$B_{\text{comm}} \times (U / 0.75 - 1)$"]
        M_GF["<b>Gross Forecast ($R_{\text{gross}}$)</b><br/>$B_{\text{comm}} + P_{\text{wt}} + A_{\text{util}}$"]
        M_NF["<b>Net Forecast ($R_{\text{net}}$)</b><br/>$R_{\text{gross}} \times 0.95$"]

        M_CB & M_WP & M_UA --> M_GF --> M_NF
    end

    subgraph RiskPillar["3. COVERAGE & CONCENTRATION RATIOS"]
        M_FWD["<b>Forward Revenue ($R_{\text{fwd}}$)</b><br/>$B_{\text{comm}} + P_{\text{wt}}$"]
        M_FCov["<b>Forward Coverage</b><br/>$(R_{\text{fwd}} / R_{\text{bdg}}) \times 100$"]
        M_CCov["<b>Committed Coverage</b><br/>$(B_{\text{comm}} / R_{\text{net}}) \times 100$"]
        M_PDep["<b>Pipeline Dependency</b><br/>$(P_{\text{wt}} / R_{\text{fwd}}) \times 100$"]

        M_CB & M_WP --> M_FWD --> M_FCov & M_PDep
        M_CB & M_NF --> M_CCov
    end

    RevenuePillar --> RiskPillar
    ForecastPillar --> RiskPillar

    style RevenuePillar fill:#EFF6FF,stroke:#2563EB,stroke-width:2px,color:#1E40AF
    style ForecastPillar fill:#FAF5FF,stroke:#9333EA,stroke-width:2px,color:#6B21A8
    style RiskPillar fill:#ECFDF5,stroke:#059669,stroke-width:2px,color:#065F46
```

---

## Master Metric Glossary & Formulas

### 1. Revenue Performance & Engagement Economics

| Metric Name | Mathematical Formula | Units | Healthy Benchmark | Diagnostic Use Case |
|:------------|:---------------------|:-----:|:-----------------:|:--------------------|
| **Actual Revenue** | $\sum \text{actual\_revenue}$ | INR | $\ge \text{Budget}$ | Total recognized fee revenue delivered to date |
| **Budget Target** | $\sum \text{revenue\_budget}$ | INR | Baseline | Operating plan revenue target approved by leadership |
| **Budget Gap** | $\text{Actual} - \text{Budget}$ | INR | $\ge 0.0$ | Dollar surplus (positive) or deficit (negative) vs plan |
| **Budget Gap %** | $(\text{Budget Gap} / \text{Budget}) \times 100$ | $\%$ | $\ge 0.0\%$ | Normalized performance percentage against plan |
| **Direct Consulting Cost** | $\sum \text{actual\_cost}$ | INR | $\le 0.60 \times \text{Rev}$ | Total direct labor and contractor costs |
| **Gross Margin (INR)** | $\text{Actual Revenue} - \text{Direct Cost}$ | INR | $\ge 0.40 \times \text{Rev}$ | Total practice contribution profit |
| **Gross Margin %** | $(\text{Gross Margin} / \text{Actual Revenue}) \times 100$ | $\%$ | $\ge 40.0\%$ | Practice profitability efficiency |

### 2. Forward Book, Coverage & Quality Ratios

| Metric Name | Mathematical Formula | Units | Healthy Benchmark | Diagnostic Use Case |
|:------------|:---------------------|:-----:|:-----------------:|:--------------------|
| **Committed Backlog** | $\sum \text{pipeline\_value} \text{ [In Delivery, Closed Won]}$ | INR | Maximum | Contractually locked engagement revenue |
| **Weighted Pipeline** | $\sum (\text{pipeline\_value} \times \text{win\_probability})$ | INR | Secondary | Expected probability value of open proposals |
| **Forward Revenue** | $\text{Committed Backlog} + \text{Weighted Pipeline}$ | INR | $\ge \text{Budget}$ | Total available forward book of business |
| **Forward Coverage**| $(\text{Forward Revenue} / \text{Budget}) \times 100$ | $\%$ | $\ge 120.0\%$ | Forward capacity relative to target budget |
| **Committed Forecast Coverage** | $(\text{Committed Backlog} / \text{Net Forecast}) \times 100$ | $\%$ | $\ge 70.0\%$ | Share of period forecast secured by signed SOWs |
| **Committed Revenue Mix** | $(\text{Committed Backlog} / \text{Forward Revenue}) \times 100$ | $\%$ | $\ge 60.0\%$ | Contract certainty ratio across entire forward book |
| **Pipeline Dependency** | $(\text{Weighted Pipeline} / \text{Forward Revenue}) \times 100$ | $\%$ | $\le 40.0\%$ | Conversion vulnerability of forward book |
| **Forecast Headroom**| $\text{Net Forecast} - \text{Budget Target}$ | INR | $> 0.0$ | Expected dollar cushion above plan |
| **Forecast Headroom %** | $(\text{Forecast Headroom} / \text{Budget Target}) \times 100$ | $\%$ | $\ge 10.0\%$ | Percentage safety buffer above operating budget |

### 3. Stochastic Monte Carlo Metrics

| Metric Name | Mathematical Definition | Units | Interpretation & Action |
|:------------|:------------------------|:-----:|:------------------------|
| **P10 Downside** | 10th percentile outcome of 5,000 runs | INR | 90% confidence floor revenue under negative conversion shocks |
| **P50 Median** | 50th percentile outcome of 5,000 runs | INR | Probabilistic median expectation under simulated volatility |
| **P90 Upside** | 90th percentile outcome of 5,000 runs | INR | Optimistic upside if high-stage proposals close early |
| **Value-at-Risk (VaR)** | $\text{Deterministic Net Forecast} - \text{P10 Outcome}$ | INR | Total quantified revenue exposed to market downside |
| **Probability > Budget** | $(\text{Count}(\text{Sim} \ge \text{Budget}) / 5000) \times 100$ | $\%$ | Empirical probability of meeting or beating operating budget |

---

## Practice Health Threshold Classification Matrix

| Health Indicator | Green (Healthy) | Amber (Watch) | Red (Critical Action) |
|:-----------------|:----------------|:--------------|:----------------------|
| **Forecast Risk** | $\text{Committed Coverage} \ge 70\%$ | $50\% \le \text{Coverage} < 70\%$ | $\text{Coverage} < 50\%$ |
| **Pipeline Risk** | $\text{Pipeline Dependency} \le 30\%$ | $30\% < \text{Dependency} \le 50\%$ | $\text{Dependency} > 50\%$ |
| **Forward Position**| $\text{Forward Coverage} \ge 120\%$ | $100\% \le \text{Coverage} < 120\%$ | $\text{Coverage} < 100\%$ |
| **Headroom Status** | $\text{Headroom \%} \ge 10.0\%$ | $0.0\% \le \text{Headroom \%} < 10.0\%$ | $\text{Headroom \%} < 0.0\%$ |
| **Performance Stance** | $\text{Budget Gap} > 0.0$ | $\text{Budget Gap} = 0.0$ | $\text{Budget Gap} < 0.0$ |

---

## Data Quality & Schema Boundaries

> [!WARNING]
> **Staffing Capacity Denominator Caveat:**
> In the current database schema, `budgets.hours_budget` represents planned billable demand rather than total consultant head-count capacity hours. Therefore, hours attainment ($\text{actual\_hours} / \text{hours\_budget}$) is displayed as **Hours vs. Budget Attainment** rather than true utilization. The system sets `data_quality.status = 'review_required'` to maintain leadership transparency.
