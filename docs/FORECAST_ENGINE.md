# X-Fin Forecast & Variance Engine Specification

> **Module Path:** `app/services/forecast_engine.py` · **Router:** `app/routers/forecast.py`

---

## Forecast Calculation Pipeline

```mermaid
flowchart TD
    subgraph S1["INPUT EXTRACTION"]
        IN_B["<b>Committed Backlog</b><br/><code>backlog_engine.calculate_backlog()</code><br/>SUM(pipeline_value) WHERE stage IN ('In Delivery', 'Closed Won')"]
        IN_P["<b>Weighted Pipeline</b><br/><code>finance_queries.get_pipeline_summary()</code><br/>SUM(pipeline_value * probability) [Latest Snapshot]"]
        IN_U["<b>Actual Utilization</b><br/><code>finance_queries.get_budget_summary()</code><br/>AVG(budgets.utilization_budget)"]
        IN_TU["<b>Target Utilization Benchmark</b><br/><code>target_utilization = 0.75</code> (75% Baseline)"]
    end

    subgraph S2["UTILIZATION ADJUSTMENT CALCULATION"]
        F_CALC["<b>1. Compute Utilization Factor</b><br/><code>factor = actual_utilization / target_utilization</code><br/><i>(e.g., 0.75 / 0.75 = 1.00)</i>"]
        UA_CALC["<b>2. Compute Utilization Adjustment</b><br/><code>adj_util = committed_backlog * (factor - 1.0)</code><br/><i>(Delta applied to committed backlog base)</i>"]
        IN_U & IN_TU --> F_CALC --> UA_CALC
        IN_B --> UA_CALC
    end

    subgraph S3["GROSS FORECAST SYNTHESIS"]
        GF_CALC["<b>3. Compute Gross Forecast</b><br/><code>gross_forecast = committed_backlog + weighted_pipeline + adj_util</code>"]
        IN_B & IN_P & UA_CALC --> GF_CALC
    end

    subgraph S4["RISK HAIRCUT CALCULATION"]
        RH_CALC["<b>4. Apply 5% Flat Execution Haircut</b><br/><code>risk_rate = 0.05</code><br/><code>adj_risk = gross_forecast * 0.05</code>"]
        GF_CALC --> RH_CALC
    end

    subgraph S5["NET FORECAST OUTPUT"]
        NF_CALC["<b>5. Compute Net Forecast Revenue</b><br/><code>forecast_revenue = round(gross_forecast - adj_risk, 2)</code>"]
        GF_CALC & RH_CALC --> NF_CALC
    end

    S1 --> S2 --> S3 --> S4 --> S5

    style S1 fill:#EFF6FF,stroke:#2563EB,stroke-width:2px,color:#1E40AF
    style S2 fill:#FDF4FF,stroke:#C026D3,stroke-width:2px,color:#86198F
    style S3 fill:#FAF5FF,stroke:#9333EA,stroke-width:2px,color:#6B21A8
    style S4 fill:#FEF2F2,stroke:#DC2626,stroke-width:2px,color:#991B1B
    style S5 fill:#ECFDF5,stroke:#059669,stroke-width:2px,color:#065F46

    style IN_B fill:#DBEAFE,stroke:#1D4ED8,stroke-width:1px,color:#1E3A8A
    style IN_P fill:#DBEAFE,stroke:#1D4ED8,stroke-width:1px,color:#1E3A8A
    style IN_U fill:#DBEAFE,stroke:#1D4ED8,stroke-width:1px,color:#1E3A8A
    style IN_TU fill:#DBEAFE,stroke:#1D4ED8,stroke-width:1px,color:#1E3A8A

    style F_CALC fill:#F5D0FE,stroke:#A21CAF,stroke-width:1px,color:#701A75
    style UA_CALC fill:#F5D0FE,stroke:#A21CAF,stroke-width:1px,color:#701A75

    style GF_CALC fill:#E9D5FF,stroke:#7E22CE,stroke-width:1px,color:#581C87
    style RH_CALC fill:#FECACA,stroke:#B91C1C,stroke-width:1px,color:#7F1D1D
    style NF_CALC fill:#A7F3D0,stroke:#047857,stroke-width:2px,color:#064E3B
```

---

## Mathematical Formulation

$$\text{Factor}_{\text{util}} = \frac{U_{\text{actual}}}{U_{\text{target}}}$$

$$\text{Adj}_{\text{util}} = \text{Backlog}_{\text{committed}} \times \left( \text{Factor}_{\text{util}} - 1.0 \right)$$

$$\text{Gross Forecast} = \text{Backlog}_{\text{committed}} + \text{Pipeline}_{\text{weighted}} + \text{Adj}_{\text{util}}$$

$$\text{Adj}_{\text{risk}} = \text{Gross Forecast} \times 0.05$$

$$\text{Forecast Revenue} = \text{Gross Forecast} - \text{Adj}_{\text{risk}}$$

---

## Input & Output Parameter Specifications

### Input Parameters

| Parameter Name | Python Type | Default Value | Source Query | Description |
|:---------------|:-----------:|:-------------:|:-------------|:------------|
| `committed_backlog` | `float` | Required | `backlog_engine.calculate_backlog()` | Sum of deals in `In Delivery` and `Closed Won` stages |
| `weighted_pipeline` | `float` | Required | `finance_queries.get_pipeline_summary()` | Probability-weighted sum of active pipeline deals |
| `utilization` | `float` | `0.74` | `finance_queries.get_budget_summary()` | Current billable staffing utilization rate |
| `target_utilization` | `float` | `0.75` | Hard-coded Constant | Benchmark target utilization rate (Raises `ValueError` if <= 0) |
| `risk_rate` | `float` | `0.05` | Hard-coded Constant | Standard 5% execution risk discount |

### Output Dataclass (`ForecastResult`)

| Field Name | Type | Precision | Example Value | Description |
|:-----------|:----:|:---------:|:--------------|:------------|
| `committed_backlog` | `float` | 2 decimal places | `100000.00` | Input committed backlog volume |
| `weighted_pipeline` | `float` | 2 decimal places | `50000.00` | Input probability-weighted pipeline |
| `utilization_adjustment` | `float` | 2 decimal places | `0.00` | Revenue adjustment derived from utilization delta |
| `risk_adjustment` | `float` | 2 decimal places | `7500.00` | 5% execution risk haircut |
| `forecast_revenue` | `float` | 2 decimal places | `142500.00` | **Final net deliverable forecast revenue** |

---

## Numerical Trace Verification

```mermaid
graph TD
    subgraph Given["Given Financial State"]
        G1["Committed Backlog: INR 100,000.00"]
        G2["Weighted Pipeline: INR 50,000.00"]
        G3["Actual Utilization: 0.75 (75%)"]
        G4["Target Utilization: 0.75 (75%)"]
        G5["Risk Rate: 0.05 (5%)"]
    end

    subgraph StepTrace["Step-by-Step Execution Trace"]
        T1["1. Factor = 0.75 / 0.75 = 1.00"]
        T2["2. Util Adj = 100,000 * (1.00 - 1.0) = INR 0.00"]
        T3["3. Gross = 100,000 + 50,000 + 0 = INR 150,000.00"]
        T4["4. Risk Haircut = 150,000 * 0.05 = INR 7,500.00"]
        T5["5. Net Forecast = 150,000 - 7,500 = INR 142,500.00"]
    end

    Given --> StepTrace

    style Given fill:#EFF6FF,stroke:#2563EB,stroke-width:2px,color:#1E40AF
    style StepTrace fill:#ECFDF5,stroke:#059669,stroke-width:2px,color:#065F46

    style G1 fill:#DBEAFE,stroke:#1D4ED8,stroke-width:1px,color:#1E3A8A
    style G2 fill:#DBEAFE,stroke:#1D4ED8,stroke-width:1px,color:#1E3A8A
    style G3 fill:#DBEAFE,stroke:#1D4ED8,stroke-width:1px,color:#1E3A8A
    style G4 fill:#DBEAFE,stroke:#1D4ED8,stroke-width:1px,color:#1E3A8A
    style G5 fill:#DBEAFE,stroke:#1D4ED8,stroke-width:1px,color:#1E3A8A

    style T1 fill:#D1FAE5,stroke:#047857,stroke-width:1px,color:#064E3B
    style T2 fill:#D1FAE5,stroke:#047857,stroke-width:1px,color:#064E3B
    style T3 fill:#D1FAE5,stroke:#047857,stroke-width:1px,color:#064E3B
    style T4 fill:#FECACA,stroke:#DC2626,stroke-width:1px,color:#991B1B
    style T5 fill:#A7F3D0,stroke:#047857,stroke-width:2px,color:#064E3B
```

> **Automated Verification:** Validated by `pytest tests/test_forecast.py`.

---

## Utilization Sensitivity Model

```mermaid
graph LR
    subgraph Scenarios["Sensitivity on INR 100,000 Backlog (Target = 75%)"]
        U1["Actual = 80% (+5% Upside)<br/>Factor = 1.0667<br/>Util Adj = +INR 6,666.67"]
        U2["Actual = 75% (Target)<br/>Factor = 1.0000<br/>Util Adj = INR 0.00"]
        U3["Actual = 70% (-5% Downside)<br/>Factor = 0.9333<br/>Util Adj = -INR 6,666.67"]
        U4["Actual = 60% (-15% Severe)<br/>Factor = 0.8000<br/>Util Adj = -INR 20,000.00"]
    end

    style Scenarios fill:#F8FAFC,stroke:#475569,stroke-width:2px,color:#1E293B
    style U1 fill:#DCFCE7,stroke:#16A34A,stroke-width:2px,color:#15803D
    style U2 fill:#EFF6FF,stroke:#2563EB,stroke-width:2px,color:#1E40AF
    style U3 fill:#FEF3C7,stroke:#D97706,stroke-width:2px,color:#92400E
    style U4 fill:#FEE2E2,stroke:#DC2626,stroke-width:2px,color:#991B1B
```

---

## Variance Engine & Bridge Decomposition

The variance engine (`app/services/variance_engine.py`) provides exact variance calculation and waterfall bridge analysis:

```mermaid
flowchart TD
    subgraph Bridge["Waterfall Variance Bridge Decomposition"]
        B_BUDGET["Budget Revenue Target"]
        V_SLIP["- Project Slippage Delta"]
        V_PIPE["+/- Pipeline Conversion Delta"]
        V_UTIL["+/- Staffing Utilization Delta"]
        V_RATE["+/- Hourly Billing Rate Delta"]
        V_UNEXP["+/- Unexplained Residual Variance"]
        B_ACTUAL["= Final Delivered Actual Revenue"]

        B_BUDGET --> V_SLIP --> V_PIPE --> V_UTIL --> V_RATE --> V_UNEXP --> B_ACTUAL
    end

    style Bridge fill:#F8FAFC,stroke:#334155,stroke-width:2px,color:#0F172A
    style B_BUDGET fill:#DBEAFE,stroke:#1E40AF,stroke-width:2px,color:#1E3A8A
    style V_SLIP fill:#FEE2E2,stroke:#DC2626,stroke-width:1px,color:#991B1B
    style V_PIPE fill:#FEF3C7,stroke:#D97706,stroke-width:1px,color:#92400E
    style V_UTIL fill:#EDE9FE,stroke:#7C3AED,stroke-width:1px,color:#5B21B6
    style V_RATE fill:#EDE9FE,stroke:#7C3AED,stroke-width:1px,color:#5B21B6
    style V_UNEXP fill:#E2E8F0,stroke:#64748B,stroke-width:1px,color:#334155
    style B_ACTUAL fill:#DCFCE7,stroke:#16A34A,stroke-width:2px,color:#15803D
```

### Variance Calculation Formulas (`VarianceResult`)

| Metric Field | Precision | Exact Formula | Functional Description |
|:-------------|:---------:|:--------------|:-----------------------|
| `actual_vs_budget` | `Decimal(2dp)` | `Actual - Budget` | Absolute variance delivered against budget |
| `actual_vs_budget_pct` | `Decimal(2dp)` | `(Actual - Budget) / Budget * 100` | Percentage variance delivered against budget |
| `forecast_vs_budget` | `Decimal(2dp)` | `Forecast - Budget` | Expected variance at period completion |
| `forecast_vs_budget_pct`| `Decimal(2dp)` | `(Forecast - Budget) / Budget * 100` | Projected percentage variance at completion |

---

## Scenario Simulation Logic

`app/services/scenario_engine.py` models revenue sensitivities against delivery and market variables:

```mermaid
flowchart LR
    P_IN["Pipeline Revenue"] -->|"*(1 + conversion_change)"| P_ADJ["Adjusted Pipeline"]
    B_IN["Base Revenue"] -->|"* ((util + util_change)/util) * (1 + rate_change)"| B_ADJ["Adjusted Delivery Base"]

    P_ADJ & B_ADJ --> COMB["Combined Pre-Slippage Revenue"]
    COMB -->|"*(1 - slippage_rate)"| SCENARIO["Net Scenario Revenue"]
    SCENARIO & B_IN --> DELTA["Revenue Delta & Percentage Change"]

    style P_IN fill:#E2E8F0,stroke:#334155,stroke-width:1px,color:#0F172A
    style B_IN fill:#E2E8F0,stroke:#334155,stroke-width:1px,color:#0F172A
    style P_ADJ fill:#FEF3C7,stroke:#D97706,stroke-width:1px,color:#92400E
    style B_ADJ fill:#EDE9FE,stroke:#7C3AED,stroke-width:1px,color:#5B21B6
    style COMB fill:#DBEAFE,stroke:#2563EB,stroke-width:1px,color:#1E40AF
    style SCENARIO fill:#DCFCE7,stroke:#16A34A,stroke-width:2px,color:#15803D
    style DELTA fill:#A7F3D0,stroke:#059669,stroke-width:1px,color:#065F46
```
