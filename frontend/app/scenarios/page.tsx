"use client";

import { useEffect, useState } from "react";

import Sidebar from "@/components/Sidebar";
import {
  getForecast,
  getVariance,
  runScenario,
} from "@/lib/api";

interface ScenarioResult {
  base_revenue: number;
  adjusted_pipeline: number;
  adjusted_utilization: number;
  scenario_revenue: number;
  revenue_change: number;
  revenue_change_pct: number;
}

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

function parseInput(value: string): number | null {
  if (value.trim() === "") {
    return null;
  }

  const parsed = Number(value);

  return Number.isFinite(parsed) ? parsed : null;
}

export default function ScenariosPage() {
  const [utilization, setUtilization] = useState("74");
  const [targetUtilization, setTargetUtilization] =
    useState("75");
  const [executionRisk, setExecutionRisk] =
    useState("5");
  const [pipelineConversion, setPipelineConversion] =
    useState("100");

  const [result, setResult] =
    useState<ScenarioResult | null>(null);

  const [baseRevenue, setBaseRevenue] =
    useState<number | null>(null);

  const [pipelineRevenue, setPipelineRevenue] =
    useState<number | null>(null);

  const [budgetRevenue, setBudgetRevenue] =
    useState<number | null>(null);

  const [loading, setLoading] = useState(false);
  const [loadingInputs, setLoadingInputs] =
    useState(true);

  const [error, setError] =
    useState<string | null>(null);

  /*
   * Load the canonical operating forecast and budget.
   *
   * Scenario engine inputs:
   * base_revenue     = committed backlog
   * pipeline_revenue = weighted pipeline
   *
   * Both come from /forecast/current.
   * Budget comes from /analytics/variance.
   */
  useEffect(() => {
    async function loadInputs() {
      try {
        setLoadingInputs(true);
        setError(null);

        const [
          forecastResponse,
          varianceResponse,
        ] = await Promise.all([
          getForecast(),
          getVariance(),
        ]);

        setBaseRevenue(
          forecastResponse.backlog.committed_backlog
        );

        setPipelineRevenue(
          forecastResponse.pipeline.weighted_pipeline
        );

        setBudgetRevenue(
          varianceResponse.budget
        );
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Unable to load scenario inputs."
        );
      } finally {
        setLoadingInputs(false);
      }
    }

    loadInputs();
  }, []);

  async function handleRunScenario() {
    if (
      baseRevenue === null ||
      pipelineRevenue === null
    ) {
      setError(
        "Scenario inputs are not available yet."
      );
      return;
    }

    const currentUtilizationValue =
      parseInput(utilization);

    const targetUtilizationValue =
      parseInput(targetUtilization);

    const executionRiskValue =
      parseInput(executionRisk);

    const pipelineConversionValue =
      parseInput(pipelineConversion);

    if (
      currentUtilizationValue === null ||
      targetUtilizationValue === null ||
      executionRiskValue === null ||
      pipelineConversionValue === null
    ) {
      setError(
        "All scenario inputs must contain valid numeric values."
      );
      return;
    }

    if (
      currentUtilizationValue < 0 ||
      currentUtilizationValue > 100 ||
      targetUtilizationValue < 0 ||
      targetUtilizationValue > 100 ||
      executionRiskValue < 0 ||
      executionRiskValue > 100 ||
      pipelineConversionValue < 0 ||
      pipelineConversionValue > 200
    ) {
      setError(
        "Scenario inputs are outside their permitted ranges."
      );
      return;
    }

    const currentUtilizationRate =
      currentUtilizationValue / 100;

    const targetUtilizationRate =
      targetUtilizationValue / 100;

    const executionRiskRate =
      executionRiskValue / 100;

    const pipelineConversionRate =
      pipelineConversionValue / 100;

    /*
     * The backend expects changes relative to the
     * 100% pipeline-conversion baseline and the
     * current utilization assumption.
     */
    const payload = {
      base_revenue: baseRevenue,
      pipeline_revenue: pipelineRevenue,
      utilization: currentUtilizationRate,
      pipeline_conversion_change:
        pipelineConversionRate - 1,
      utilization_change:
        targetUtilizationRate -
        currentUtilizationRate,
      billing_rate_change: 0,
      slippage_rate: executionRiskRate,
    };

    setLoading(true);
    setError(null);

    try {
      const response =
        await runScenario(payload);

      setResult(response as ScenarioResult);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to run scenario."
      );

      setResult(null);
    } finally {
      setLoading(false);
    }
  }

  function resetScenario() {
    setUtilization("74");
    setTargetUtilization("75");
    setExecutionRisk("5");
    setPipelineConversion("100");
    setResult(null);
    setError(null);
  }

  const scenarioForecast =
    result?.scenario_revenue ?? null;

  const scenarioVariance =
    result?.revenue_change ?? null;

  const scenarioVariancePct =
    result?.revenue_change_pct ?? null;

  /*
   * Separate from the scenario engine's
   * "revenue change" metric, which is measured
   * against the engine's base position.
   */
  const scenarioVsBudget =
    result !== null && budgetRevenue !== null
      ? result.scenario_revenue - budgetRevenue
      : null;

  const scenarioVsBudgetPct =
    result !== null &&
    budgetRevenue !== null &&
    budgetRevenue !== 0
      ? ((result.scenario_revenue -
          budgetRevenue) /
          budgetRevenue) *
        100
      : null;

  /*
   * The Scenario API does not expose a separate
   * execution/slippage adjustment.
   *
   * This residual reconciles the returned result:
   *
   * scenario revenue
   * - base revenue
   * - adjusted pipeline
   * - adjusted utilization
   */
  const impliedExecutionAdjustment =
    result !== null
      ? result.scenario_revenue -
        result.base_revenue -
        result.adjusted_pipeline -
        result.adjusted_utilization
      : null;

  return (
    <main className="app-shell">
      <Sidebar />

      <section className="main-content">
        <header className="topbar">
          <div>
            <div className="eyebrow">
              DELIVERY FINANCE
            </div>

            <h1>Scenarios</h1>
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
          <section className="scenario-intro">
            <div>
              <div className="section-kicker">
                MANAGEMENT ANALYSIS
              </div>

              <h2>Scenario analysis</h2>

              <p>
                Adjust operating assumptions to
                examine their effect on forward
                revenue.
              </p>
            </div>
          </section>

          <section className="section">
            <div className="section-header">
              <div>
                <div className="section-kicker">
                  ASSUMPTIONS
                </div>

                <h2>Scenario inputs</h2>
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
                      value={targetUtilization}
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
                    used by the scenario engine.
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
                    Slippage rate applied to the
                    scenario.
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
                      value={pipelineConversion}
                      onChange={(event) =>
                        setPipelineConversion(
                          event.target.value
                        )
                      }
                    />

                    <span>%</span>
                  </div>

                  <p>
                    Conversion level applied to the
                    weighted pipeline baseline.
                  </p>
                </div>

                <div className="scenario-actions">
                  <button
                    className="primary-button"
                    onClick={handleRunScenario}
                    disabled={
                      loading ||
                      loadingInputs ||
                      baseRevenue === null ||
                      pipelineRevenue === null
                    }
                  >
                    {loading
                      ? "Running..."
                      : loadingInputs
                        ? "Loading inputs..."
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
                    BASE POSITION
                  </div>

                  <div className="scenario-summary-list">
                    <div className="scenario-summary-item">
                      <span>
                        Committed backlog
                      </span>

                      <strong>
                        {baseRevenue !== null
                          ? formatCr(baseRevenue)
                          : "—"}
                      </strong>
                    </div>

                    <div className="scenario-summary-item">
                      <span>
                        Weighted pipeline
                      </span>

                      <strong>
                        {pipelineRevenue !== null
                          ? formatCr(
                              pipelineRevenue
                            )
                          : "—"}
                      </strong>
                    </div>

                    <div className="scenario-summary-item">
                      <span>
                        Budget
                      </span>

                      <strong>
                        {budgetRevenue !== null
                          ? formatCr(
                              budgetRevenue
                            )
                          : "—"}
                      </strong>
                    </div>
                  </div>

                  <div className="panel-label">
                    METHOD
                  </div>

                  <p>
                    The scenario modifies the
                    operating assumptions supplied
                    to the scenario engine. Base
                    revenue and weighted pipeline are
                    taken from the current X-Fin
                    forecast position.
                  </p>
                </div>
              </div>
            </div>
          </section>

          {error && (
            <section className="section">
              <div className="scenario-error">
                <div className="scenario-error-title">
                  Scenario could not be completed
                </div>

                <p>{error}</p>
              </div>
            </section>
          )}

          {result && (
            <>
              <section className="section">
                <div className="section-header">
                  <div>
                    <div className="section-kicker">
                      RESULT
                    </div>

                    <h2>Scenario outcome</h2>
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
                      {scenarioForecast !== null
                        ? formatCr(
                            scenarioForecast
                          )
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
                      {budgetRevenue !== null
                        ? formatCr(
                            budgetRevenue
                          )
                        : "—"}
                    </div>

                    <div className="metric-secondary">
                      Revenue plan
                    </div>
                  </div>

                  <div className="metric-block">
                    <div className="metric-label">
                      Variance vs budget
                    </div>

                    <div className="metric-value">
                      {scenarioVsBudget !== null
                        ? formatCr(
                            scenarioVsBudget
                          )
                        : "—"}
                    </div>

                    <div className="metric-secondary">
                      {scenarioVsBudgetPct !== null
                        ? `${formatPercent(
                            scenarioVsBudgetPct
                          )} vs budget`
                        : "Budget comparison unavailable"}
                    </div>
                  </div>

                  <div className="metric-block">
                    <div className="metric-label">
                      Change from base
                    </div>

                    <div className="metric-value">
                      {scenarioVariance !== null
                        ? formatCr(
                            scenarioVariance
                          )
                        : "—"}
                    </div>

                    <div className="metric-secondary">
                      {scenarioVariancePct !== null
                        ? `${formatPercent(
                            scenarioVariancePct
                          )} relative change`
                        : "Relative change unavailable"}
                    </div>
                  </div>
                </div>
              </section>

              <section className="section">
                <div className="section-header">
                  <div>
                    <div className="section-kicker">
                      SCENARIO BRIDGE
                    </div>

                    <h2>Scenario construction</h2>
                  </div>

                  <div className="section-meta">
                    Backend-calculated adjustments
                  </div>
                </div>

                <div className="panel scenario-result-panel">
                  <div className="scenario-result-row">
                    <span>
                      Base revenue
                    </span>

                    <strong>
                      {formatCurrency(
                        result.base_revenue
                      )}
                    </strong>
                  </div>

                  <div className="scenario-result-row">
                    <span>
                      Adjusted pipeline
                    </span>

                    <strong>
                      {formatCurrency(
                        result.adjusted_pipeline
                      )}
                    </strong>
                  </div>

                  <div className="scenario-result-row">
                    <span>
                      Utilization adjustment
                    </span>

                    <strong>
                      {formatCurrency(
                        result.adjusted_utilization
                      )}
                    </strong>
                  </div>

                  <div className="scenario-result-row">
                    <span>
                      Implied execution adjustment
                    </span>

                    <strong>
                      {impliedExecutionAdjustment !==
                      null
                        ? formatCurrency(
                            impliedExecutionAdjustment
                          )
                        : "—"}
                    </strong>
                  </div>

                  <div className="scenario-result-total">
                    <span>
                      Scenario forecast
                    </span>

                    <strong>
                      {formatCurrency(
                        result.scenario_revenue
                      )}
                    </strong>
                  </div>
                </div>
              </section>

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

                  <div className="observation">
                    <span className="observation-index">
                      04
                    </span>

                    <p>
                      The scenario changes forward
                      revenue by{" "}
                      <strong>
                        {formatCr(
                          result.revenue_change
                        )}
                      </strong>{" "}
                      (
                      <strong>
                        {formatPercent(
                          result.revenue_change_pct
                        )}
                      </strong>
                      ) relative to the scenario
                      engine's base position.
                    </p>
                  </div>

                  {budgetRevenue !== null &&
                    scenarioForecast !== null &&
                    scenarioVsBudget !== null &&
                    scenarioVsBudgetPct !== null && (
                      <div className="observation">
                        <span className="observation-index">
                          05
                        </span>

                        <p>
                          The resulting scenario
                          forecast is{" "}
                          <strong>
                            {formatCr(
                              scenarioForecast
                            )}
                          </strong>
                          , representing a{" "}
                          <strong>
                            {formatCr(
                              scenarioVsBudget
                            )}
                          </strong>{" "}
                          variance versus the{" "}
                          <strong>
                            {formatCr(
                              budgetRevenue
                            )}
                          </strong>{" "}
                          budget (
                          <strong>
                            {formatPercent(
                              scenarioVsBudgetPct
                            )}
                          </strong>
                          ).
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