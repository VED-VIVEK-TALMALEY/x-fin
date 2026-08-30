# X-Fin Forecast & Variance Engine Specification

> **Module Paths:** `app/services/forecast_engine.py`, `app/services/forecast_decomposition.py`, `app/services/monte_carlo_engine.py`, `app/services/variance_engine.py`

---

## Forecast Calculation Pipeline

```mermaid
flowchart TD
    subgraph S1["1. INPUT INGESTION & DATA SANITIZATION"]
        IN_B["<b>Committed Backlog ($B_{comm}$)</b><br/><code>backlog_engine.calculate_backlog()</code><br/>SUM(pipeline_value) WHERE stage IN ('In Delivery', 'Closed Won')"]
        IN_P["<b>Weighted Pipeline ($P_{wt}$)</b><br/><code>finance_queries.get_pipeline_summary()</code><br/>SUM(pipeline_value * probability) [Latest Snapshot]"]
        IN_U["<b>Actual Utilization ($U_{act}$)</b><br/><code>finance_queries.get_budget_summary()</code><br/>AVG(budgets.utilization_budget)"]
        IN_TU["<b>Target Utilization Benchmark ($U_{tgt}$)</b><br/>Fixed Constant: <code>target_utilization = 0.75</code> (75%)"]
    end

    subgraph S2["2. UTILIZATION FACTOR & ADJUSTMENT CALCULATION"]
        F_CALC["<b>1. Compute Utilization Factor</b><br/>$$\text{Factor}_{\text{util}} = \frac{U_{\text{act}}}{U_{\text{tgt}}}$$<br/><i>(e.g., 0.75 / 0.75 = 1.00)</i>"]
        UA_CALC["<b>2. Compute Utilization Adjustment</b><br/>$$\text{Adj}_{\text{util}} = B_{\text{comm}} \times (\text{Factor}_{\text{util}} - 1.0)$$<br/><i>(Positive = Staffing Over-Utilization Upside; Negative = Under-Utilization Drag)</i>"]
        IN_U & IN_TU --> F_CALC --> UA_CALC
        IN_B --> UA_CALC
    end

    subgraph S3["3. GROSS FORECAST SYNTHESIS"]
        GF_CALC["<b>3. Compute Gross Forecast Revenue</b><br/>$$R_{\text{gross}} = B_{\text{comm}} + P_{\text{wt}} + \text{Adj}_{\text{util}}$$"]
        IN_B & IN_P & UA_CALC --> GF_CALC
    end

    subgraph S4["4. EXECUTION RISK HAIRCUT"]
        RH_CALC["<b>4. Apply 5% Flat Execution Haircut</b><br/>$$\text{Adj}_{\text{risk}} = R_{\text{gross}} \times 0.05$$<br/><i>(Protects against scope slip & delivery delays)</i>"]
        GF_CALC --> RH_CALC
    end

    subgraph S5["5. NET DELIVERABLE FORECAST"]
        NF_CALC["<b>5. Compute Net Forecast Revenue</b><br/>$$R_{\text{net}} = \text{round}(R_{\text{gross}} - \text{Adj}_{\text{risk}}, 2)$$"]
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

### 1. Utilization Multiplier & Adjustment

$$\text{Factor}_{\text{util}} = \frac{U_{\text{actual}}}{U_{\text{target}}}$$

$$\text{Adj}_{\text{util}} = \text{Backlog}_{\text{committed}} \times \left( \text{Factor}_{\text{util}} - 1.0 \right)$$

### 2. Gross Forecast Synthesis

$$\text{Gross Forecast} = \text{Backlog}_{\text{committed}} + \text{Pipeline}_{\text{weighted}} + \text{Adj}_{\text{util}}$$

### 3. Execution Risk Haircut

$$\text{Adj}_{\text{risk}} = \text{Gross Forecast} \times 0.05$$

### 4. Net Deliverable Forecast Revenue

$$\text{Forecast Revenue} = \text{Gross Forecast} - \text{Adj}_{\text{risk}}$$

---

## Numerical Step-by-Step Trace Matrix

| Step Number | Calculation Stage | Mathematical Operation | Baseline Numerical Inputs | Computed Output |
|:-----------:|:------------------|:-----------------------|:--------------------------|:----------------|
| **1** | Backlog Ingestion | Extract locked contract value | Sum of In Delivery + Closed Won | **INR 100,000.00** |
| **2** | Pipeline Weighting | $\sum (\text{Value} \times \text{Probability})$ | Sum of active commercial proposals | **INR 50,000.00** |
| **3** | Utilization Delta | $100,000 \times \left(\frac{0.75}{0.75} - 1.0\right)$ | Utilization at target (75.0%) | **INR 0.00** |
| **4** | Gross Synthesis | $100,000 + 50,000 + 0$ | Aggregation of revenue layers | **INR 150,000.00** |
| **5** | Risk Haircut | $150,000 \times 0.05$ | 5% delivery execution haircut | **INR -7,500.00** |
| **6** | **Net Deliverable**| $\mathbf{150,000 - 7,500}$ | **Risk-adjusted period forecast** | **INR 142,500.00** |

---

## Monte Carlo Stochastic Engine Mechanics

`app/services/monte_carlo_engine.py` executes 5,000 stochastic iterations to quantify forecast volatility:

```mermaid
flowchart LR
    subgraph Distributions["1. RANDOM VARIABLE DISTRIBUTIONS"]
        D_PIP["<b>Pipeline Conversion Rate</b><br/>Beta Distribution: $\alpha, \beta$<br/>Centered on historical stage win rates"]
        D_UTL["<b>Staffing Utilization</b><br/>Gaussian Normal Distribution<br/>$\mu = U_{\text{act}}, \sigma = 0.035$"]
        D_SLP["<b>Milestone Delivery Slippage</b><br/>Log-Normal Distribution<br/>Skewed right (0% to 15% slippage)"]
    end

    subgraph Simulation["2. STOCHASTIC SIMULATION ENGINE"]
        S_LOOP["5,000 Independent Trials (Random Seed = 42)<br/>Calculate simulated gross, haircut, and net revenue per trial"]
    end

    subgraph Quantiles["3. STATISTICAL QUANTILES & VaR"]
        Q_P10["<b>P10 (Downside)</b><br/>90% confidence floor"]
        Q_P50["<b>P50 (Median)</b><br/>Stochastic median"]
        Q_P90["<b>P90 (Upside)</b><br/>10% exceedance target"]
        Q_VAR["<b>Value-at-Risk (VaR)</b><br/>$\text{Deterministic} - \text{P10}$"]
    end

    Distributions --> Simulation --> Quantiles

    style Distributions fill:#EFF6FF,stroke:#2563EB,stroke-width:2px,color:#1E40AF
    style Simulation fill:#FAF5FF,stroke:#9333EA,stroke-width:2px,color:#6B21A8
    style Quantiles fill:#ECFDF5,stroke:#059669,stroke-width:2px,color:#065F46
```

### Monte Carlo Distribution Breakdown

| Quantile | Statistical Definition | Meaning for Practice Leadership | Remediation Playbook |
|:---------|:-----------------------|:--------------------------------|:---------------------|
| **P10** | 10th Percentile of outcomes | Stress-tested worst-case deliverable revenue | Set emergency staffing freeze & contractor cuts |
| **P50** | 50th Percentile of outcomes | Probabilistic median expectation | Benchmark against deterministic net forecast |
| **P90** | 90th Percentile of outcomes | Optimistic commercial capture | Pre-allocate recruiting & contractor pipeline |
| **VaR (P10)** | Deterministic Net - P10 | Total downside revenue at risk under market shocks | Monitor top 3 accounts for early warning signs |

---

## Variance Bridge Engine Specification

`app/services/variance_engine.py` components variances between Actual vs. Budget and Forecast vs. Budget:

```mermaid
flowchart TD
    subgraph BridgeActual["ACTUAL VS. BUDGET VARIANCE BRIDGE"]
        ACT_REV["Delivered Revenue ($R_{\text{act}}$)"]
        BDG_REV["Operating Budget ($R_{\text{bdg}}$)"]
        
        GAP_ACT["<b>Budget Gap ($\Delta_{\text{actual}}$)</b><br/>$$R_{\text{act}} - R_{\text{bdg}}$$"]
        PCT_ACT["<b>Budget Gap % ($\%_{\text{actual}}$)</b><br/>$$\left(\frac{\Delta_{\text{actual}}}{R_{\text{bdg}}}\right) \times 100$$"]
        
        ACT_REV & BDG_REV --> GAP_ACT --> PCT_ACT
    end

    subgraph BridgeForecast["FORECAST VS. BUDGET VARIANCE BRIDGE"]
        FC_REV["Net Forecast ($R_{\text{fc}}$)"]
        
        GAP_FC["<b>Forecast Headroom ($\Delta_{\text{fc}}$)</b><br/>$$R_{\text{fc}} - R_{\text{bdg}}$$"]
        PCT_FC["<b>Forecast Headroom % ($\%_{\text{fc}}$)</b><br/>$$\left(\frac{\Delta_{\text{fc}}}{R_{\text{bdg}}}\right) \times 100$$"]
        
        FC_REV & BDG_REV --> GAP_FC --> PCT_FC
    end

    style BridgeActual fill:#EFF6FF,stroke:#2563EB,stroke-width:2px,color:#1E40AF
    style BridgeForecast fill:#ECFDF5,stroke:#059669,stroke-width:2px,color:#065F46
```

### Variance Classification Matrix

| Variance Metric | Range Condition | Classification | Management Interpretation |
|:----------------|:----------------|:---------------|:--------------------------|
| **Budget Gap %** | $\ge 0.0\%$ | Ahead of Plan | Practice revenue exceeds budgeted baseline |
| **Budget Gap %** | $-10.0\% \le \text{gap} < 0.0\%$ | Within Tolerance | Minor lag; operational corrective measures required |
| **Budget Gap %** | $< -10.0\%$ | Significant Deficit | Critical delivery shortfall; partner review triggered |
| **Forecast Headroom %** | $\ge 10.0\%$ | Strong Buffer | High probability of beating annual operating plan |
| **Forecast Headroom %** | $0.0\% \le \text{gap} < 10.0\%$ | Moderate Headroom | On-plan; minor vulnerability to deal slippage |
| **Forecast Headroom %** | $< 0.0\%$ | Revenue Deficit | Forward plan insufficient to achieve approved budget |

---

## Input & Output Parameter Specifications

### Input Parameters (`build_forecast`)

| Parameter Name | Python Type | Default | Validation Constraint | Description |
|:---------------|:-----------:|:-------:|:----------------------|:------------|
| `committed_backlog` | `float` | Required | $\ge 0.0$ | Sum of pipeline values for 'In Delivery' and 'Closed Won' |
| `weighted_pipeline` | `float` | Required | $\ge 0.0$ | Sum of $(\text{pipeline\_value} \times \text{win\_probability})$ |
| `utilization` | `float` | `0.74` | $0.0 \le U \le 2.0$ | Current average consultant billable utilization rate |
| `target_utilization` | `float` | `0.75` | $> 0.0$ (Raises `ValueError` if $\le 0$) | Practice benchmark target utilization |
| `risk_rate` | `float` | `0.05` | $0.0 \le \text{rate} \le 1.0$ | Execution risk discount rate |

### Output Dataclass (`ForecastResult`)

| Field Name | Type | Precision | Sample Value | Description |
|:-----------|:----:|:---------:|:-------------|:------------|
| `committed_backlog` | `float` | 2 decimal places | `100000.00` | Input committed backlog volume |
| `weighted_pipeline` | `float` | 2 decimal places | `50000.00` | Input probability-weighted pipeline |
| `utilization_adjustment` | `float` | 2 decimal places | `0.00` | Revenue delta from utilization variance |
| `risk_adjustment` | `float` | 2 decimal places | `7500.00` | 5% execution risk haircut |
| `forecast_revenue` | `float` | 2 decimal places | `142500.00` | **Net risk-adjusted deliverable forecast** |
