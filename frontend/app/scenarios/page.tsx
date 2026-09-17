"use client";

import { useState } from "react";
import Sidebar from "@/components/Sidebar";
import { runScenario } from "@/lib/api";

/* ============================================================
   FORMATTERS
============================================================ */

function formatCurrency(value: number) {
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    notation: "compact",
    maximumFractionDigits: 1,
  }).format(value);
}

function formatPercent(value: number) {
  return `${value.toFixed(1)}%`;
}

function formatCr(value: number) {
  return `₹${(value / 10000000).toFixed(1)} Cr`;
}

/* ============================================================
   TYPES
============================================================ */

interface ScenarioResult {
  forecast_revenue?: number;
  forecast?: number;

  budget_revenue?: number;
  variance_vs_budget?: number;
  variance_vs_budget_pct?: number;

  committed_backlog?: number;
  weighted_pipeline?: number;

  utilization_adjustment?: number;
  risk_adjustment?: number;

  [key: string]: unknown;
}

/* ============================================================
   PAGE
============================================================ */

export default function ScenariosPage() {
  const [utilization, setUtilization] =
    useState("74");

  const [targetUtilization, setTargetUtilization] =
    useState("75");

  const [executionRisk, setExecutionRisk] =
    useState("5");

  const [pipelineConversion, setPipelineConversion] =
    useState("100");

  const [result, setResult] =
    useState<ScenarioResult | null>(null);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);

  const [hasRun, setHasRun] =
    useState(false);

  /* ==========================================================
     RUN SCENARIO
  ========================================================== */

  async function handleRunScenario() {
    setLoading(true);
    setError(null);

    try {
      const response = await runScenario({
        current_utilization:
          Number(utilization) / 100,

        target_utilization:
          Number(targetUtilization) / 100,

        execution_risk_rate:
          Number(executionRisk) / 100,

        pipeline_conversion_rate:
          Number(pipelineConversion) / 100,
      });

      setResult(
        response as ScenarioResult
      );

      setHasRun(true);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to run scenario."
      );
    } finally {
      setLoading(false);
    }
  }

  /* ==========================================================
     RESET
  ========================================================== */

  function resetScenario() {
    setUtilization("74");
    setTargetUtilization("75");
    setExecutionRisk("5");
    setPipelineConversion("100");

    setResult(null);
    setError(null);
    setHasRun(false);
  }

  /* ==========================================================
     RESULT HELPERS
  ========================================================== */

  const forecast =
    result?.forecast_revenue ??
    result?.forecast ??
    null;

  const budget =
    result?.budget_revenue ??
    null;

  const variance =
    result?.variance_vs_budget ??
    (forecast !== null && budget !== null
      ? forecast - budget
      : null);

  const variancePct =
    result?.variance_vs_budget_pct ??
    (variance !== null &&
    budget !== null &&
    budget !== 0
      ? (variance / budget) * 100
      : null);

  /* ==========================================================
     RENDER
  ========================================================== */

  return (
    <main className="app-shell">
      <Sidebar />

      <section className="main-content">
        {/* ==================================================
            HEADER
        ================================================== */}

        <header className="topbar">
          <div>
            <div className="eyebrow">
              DELIVERY FINANCE
            </div>

            <h1>
              Scenarios
            </h1>
          </div>

          <div className="topbar-right">
            <div className="period">
              Current period
            </div>

            <div className="period-value">
              FY2026
            </div>
          </div>
        </header>

        <div className="content">
          {/* ==================================================
              INTRO
          ================================================== */}

          <section className="scenario-intro">
            <div>
              <div className="section-kicker">
                MANAGEMENT ANALYSIS
              </div>

              <h2>
                Scenario analysis
              </h2>

              <p>
                Adjust operating assumptions to
                examine their effect on forward
                revenue.
              </p>
            </div>
          </section>

          {/* ==================================================
              SCENARIO INPUTS
          ================================================== */}

          <section className="section">
            <div className="section-header">
              <div>
                <div className="section-kicker">
                  ASSUMPTIONS
                </div>

                <h2>
                  Scenario inputs
                </h2>
              </div>

              <div className="section-meta">
                Edit assumptions and run analysis
              </div>
            </div>

            <div className="scenario-layout">
              <div className="panel scenario-input-panel">
                <div className="scenario-field">
                  <label htmlFor="utilization">
                    Current utilization
                  </label>

                  <div className="scenario-input-row">
                    <input
                      id="utilization"
                      type="number"
                      min="0"
                      max="100"
                      step="0.5"
                      value={utilization}
                      onChange={(event) =>
                        setUtilization(
                          event.target.value
                        )
                      }
                    />

                    <span>%</span>
                  </div>

                  <p>
                    Current delivery utilization
                    assumption.
                  </p>
                </div>

                <div className="scenario-field">
                  <label htmlFor="target-utilization">
                    Target utilization
                  </label>

                  <div className="scenario-input-row">
                    <input
                      id="target-utilization"
                      type="number"
                      min="0"
                      max="100"
                      step="0.5"
                      value={
                        targetUtilization
                      }
                      onChange={(event) =>
                        setTargetUtilization(
                          event.target.value
                        )
                      }
                    />

                    <span>%</span>
                  </div>

                  <p>
                    Target delivery utilization
                    used by the forecast.
                  </p>
                </div>

                <div className="scenario-field">
                  <label htmlFor="execution-risk">
                    Execution risk rate
                  </label>

                  <div className="scenario-input-row">
                    <input
                      id="execution-risk"
                      type="number"
                      min="0"
                      max="100"
                      step="0.5"
                      value={executionRisk}
                      onChange={(event) =>
                        setExecutionRisk(
                          event.target.value
                        )
                      }
                    />

                    <span>%</span>
                  </div>

                  <p>
                    Revenue haircut applied for
                    execution risk.
                  </p>
                </div>

                <div className="scenario-field">
                  <label htmlFor="pipeline-conversion">
                    Pipeline conversion
                  </label>

                  <div className="scenario-input-row">
                    <input
                      id="pipeline-conversion"
                      type="number"
                      min="0"
                      max="200"
                      step="1"
                      value={
                        pipelineConversion
                      }
                      onChange={(event) =>
                        setPipelineConversion(
                          event.target.value
                        )
                      }
                    />

                    <span>%</span>
                  </div>

                  <p>
                    Scenario adjustment applied to
                    weighted pipeline.
                  </p>
                </div>

                <div className="scenario-actions">
                  <button
                    className="primary-button"
                    onClick={
                      handleRunScenario
                    }
                    disabled={loading}
                  >
                    {loading
                      ? "Running..."
                      : "Run scenario"}
                  </button>

                  <button
                    className="secondary-button"
                    onClick={resetScenario}
                    disabled={loading}
                  >
                    Reset
                  </button>
                </div>
              </div>

              {/* ==================================================
                  ASSUMPTION SUMMARY
              ================================================== */}

              <div className="panel scenario-summary-panel">
                <div className="panel-heading">
                  <div>
                    <div className="panel-label">
                      CURRENT SCENARIO
                    </div>

                    <div className="panel-heading-title">
                      Operating assumptions
                    </div>
                  </div>
                </div>

                <div className="scenario-summary-list">
                  <div className="scenario-summary-item">
                    <span>
                      Current utilization
                    </span>

                    <strong>
                      {formatPercent(
                        Number(utilization)
                      )}
                    </strong>
                  </div>

                  <div className="scenario-summary-item">
                    <span>
                      Target utilization
                    </span>

                    <strong>
                      {formatPercent(
                        Number(
                          targetUtilization
                        )
                      )}
                    </strong>
                  </div>

                  <div className="scenario-summary-item">
                    <span>
                      Execution risk
                    </span>

                    <strong>
                      {formatPercent(
                        Number(executionRisk)
                      )}
                    </strong>
                  </div>

                  <div className="scenario-summary-item">
                    <span>
                      Pipeline conversion
                    </span>

                    <strong>
                      {formatPercent(
                        Number(
                          pipelineConversion
                        )
                      )}
                    </strong>
                  </div>
                </div>

                <div className="scenario-methodology">
                  <div className="panel-label">
                    METHOD
                  </div>

                  <p>
                    The scenario modifies the
                    operating assumptions supplied to
                    the forecast engine. The resulting
                    revenue position is returned by the
                    X-Fin API.
                  </p>
                </div>
              </div>
            </div>
          </section>

          {/* ==================================================
              ERROR
          ================================================== */}

          {error && (
            <section className="section">
              <div className="scenario-error">
                <div className="scenario-error-title">
                  Scenario could not be completed
                </div>

                <p>
                  {error}
                </p>
              </div>
            </section>
          )}

          {/* ==================================================
              RESULTS
          ================================================== */}

          {hasRun && result && (
            <>
              <section className="section">
                <div className="section-header">
                  <div>
                    <div className="section-kicker">
                      RESULT
                    </div>

                    <h2>
                      Scenario outcome
                    </h2>
                  </div>

                  <div className="section-meta">
                    Calculated from current assumptions
                  </div>
                </div>

                <div className="metric-grid">
                  <div className="metric-block">
                    <div className="metric-label">
                      Scenario forecast
                    </div>

                    <div className="metric-value">
                      {forecast !== null
                        ? formatCr(forecast)
                        : "—"}
                    </div>

                    <div className="metric-secondary">
                      Forward revenue
                    </div>
                  </div>

                  <div className="metric-block">
                    <div className="metric-label">
                      Budget
                    </div>

                    <div className="metric-value">
                      {budget !== null
                        ? formatCr(budget)
                        : "—"}
                    </div>

                    <div className="metric-secondary">
                      Revenue plan
                    </div>
                  </div>

                  <div className="metric-block">
                    <div className="metric-label">
                      Variance
                    </div>

                    <div className="metric-value">
                      {variance !== null
                        ? formatCr(variance)
                        : "—"}
                    </div>

                    <div className="metric-secondary">
                      Scenario forecast vs budget
                    </div>
                  </div>

                  <div className="metric-block">
                    <div className="metric-label">
                      Variance %
                    </div>

                    <div className="metric-value">
                      {variancePct !== null
                        ? formatPercent(
                            variancePct
                          )
                        : "—"}
                    </div>

                    <div className="metric-secondary">
                      Relative to budget
                    </div>
                  </div>
                </div>
              </section>

              {/* ==================================================
                  FORECAST BRIDGE
              ================================================== */}

              <section className="section">
                <div className="section-header">
                  <div>
                    <div className="section-kicker">
                      FORECAST BRIDGE
                    </div>

                    <h2>
                      Scenario construction
                    </h2>
                  </div>
                </div>

                <div className="panel scenario-result-panel">
                  <div className="scenario-result-row">
                    <span>
                      Committed backlog
                    </span>

                    <strong>
                      {result.committed_backlog !==
                      undefined
                        ? formatCurrency(
                            result.committed_backlog
                          )
                        : "—"}
                    </strong>
                  </div>

                  <div className="scenario-result-row">
                    <span>
                      Weighted pipeline
                    </span>

                    <strong>
                      {result.weighted_pipeline !==
                      undefined
                        ? formatCurrency(
                            result.weighted_pipeline
                          )
                        : "—"}
                    </strong>
                  </div>

                  <div className="scenario-result-row">
                    <span>
                      Utilization adjustment
                    </span>

                    <strong>
                      {result.utilization_adjustment !==
                      undefined
                        ? formatCurrency(
                            result.utilization_adjustment
                          )
                        : "—"}
                    </strong>
                  </div>

                  <div className="scenario-result-row">
                    <span>
                      Execution adjustment
                    </span>

                    <strong>
                      {result.risk_adjustment !==
                      undefined
                        ? formatCurrency(
                            result.risk_adjustment
                          )
                        : "—"}
                    </strong>
                  </div>

                  <div className="scenario-result-total">
                    <span>
                      Scenario forecast
                    </span>

                    <strong>
                      {forecast !== null
                        ? formatCurrency(forecast)
                        : "—"}
                    </strong>
                  </div>
                </div>
              </section>

              {/* ==================================================
                  INTERPRETATION
              ================================================== */}

              <section className="section last-section">
                <div className="section-header">
                  <div>
                    <div className="section-kicker">
                      ANALYSIS
                    </div>

                    <h2>
                      Scenario interpretation
                    </h2>
                  </div>
                </div>

                <div className="observations">
                  <div className="observation">
                    <span className="observation-index">
                      01
                    </span>

                    <p>
                      The scenario uses a current
                      utilization assumption of{" "}
                      <strong>
                        {formatPercent(
                          Number(utilization)
                        )}
                      </strong>{" "}
                      against a target of{" "}
                      <strong>
                        {formatPercent(
                          Number(
                            targetUtilization
                          )
                        )}
                      </strong>
                      .
                    </p>
                  </div>

                  <div className="observation">
                    <span className="observation-index">
                      02
                    </span>

                    <p>
                      The execution risk assumption
                      is{" "}
                      <strong>
                        {formatPercent(
                          Number(executionRisk)
                        )}
                      </strong>
                      .
                    </p>
                  </div>

                  <div className="observation">
                    <span className="observation-index">
                      03
                    </span>

                    <p>
                      Pipeline conversion is set to{" "}
                      <strong>
                        {formatPercent(
                          Number(
                            pipelineConversion
                          )
                        )}
                      </strong>
                      .
                    </p>
                  </div>

                  {forecast !== null &&
                    budget !== null && (
                      <div className="observation">
                        <span className="observation-index">
                          04
                        </span>

                        <p>
                          The resulting scenario
                          forecast is{" "}
                          <strong>
                            {formatCr(
                              forecast
                            )}
                          </strong>
                          , compared with a budget
                          of{" "}
                          <strong>
                            {formatCr(
                              budget
                            )}
                          </strong>
                          .
                        </p>
                      </div>
                    )}
                </div>
              </section>
            </>
          )}
        </div>
      </section>
    </main>
  );
}