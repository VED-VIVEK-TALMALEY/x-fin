"use client";

import { useEffect, useMemo, useState } from "react";

import {
  getForecast,
  getVariance,
  getIntelligence,
} from "@/lib/api";

import type { ForecastCurrentResponse } from "@/types/forecast";
import type { VarianceResponse } from "@/types/analytics";
import type { IntelligenceOverview } from "@/types/intelligence";

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
  return `${value >= 0 ? "+" : ""}${value.toFixed(1)}%`;
}

function formatPlainPercent(value: number) {
  return `${value.toFixed(1)}%`;
}

/* ============================================================
   FORECAST BRIDGE
============================================================ */

function ForecastBridge({
  forecast,
}: {
  forecast: ForecastCurrentResponse;
}) {
  const items = [
    {
      label: "Committed backlog",
      value: forecast.forecast.committed_backlog,
      operator: "",
      type: "positive",
    },
    {
      label: "Weighted pipeline",
      value: forecast.forecast.weighted_pipeline,
      operator: "+",
      type: "positive",
    },
    {
      label: "Utilization adjustment",
      value: forecast.forecast.utilization_adjustment,
      operator:
        forecast.forecast.utilization_adjustment >= 0
          ? "+"
          : "−",
      type:
        forecast.forecast.utilization_adjustment >= 0
          ? "positive"
          : "negative",
    },
    {
      label: "Execution risk",
      value: -Math.abs(
        forecast.forecast.risk_adjustment
      ),
      operator: "−",
      type: "negative",
    },
  ];

  const maxValue = Math.max(
    ...items.map((item) => Math.abs(item.value))
  );

  return (
    <div className="forecast-bridge">
      {items.map((item, index) => {
        const width =
          maxValue > 0
            ? Math.max(
                (Math.abs(item.value) / maxValue) * 100,
                5
              )
            : 5;

        return (
          <div
            className="bridge-row"
            key={item.label}
          >
            <div className="bridge-label">
              <span>{item.label}</span>

              <span
                className={
                  item.type === "negative"
                    ? "bridge-negative"
                    : "bridge-positive"
                }
              >
                {item.value < 0 ? "−" : ""}
                {formatCurrency(
                  Math.abs(item.value)
                )}
              </span>
            </div>

            <div className="bridge-track">
              <div
                className={`bridge-bar ${item.type}`}
                style={{
                  width: `${width}%`,
                }}
              />
            </div>

            {index < items.length - 1 && (
              <div className="bridge-operator">
                {items[index + 1].operator}
              </div>
            )}
          </div>
        );
      })}

      <div className="bridge-total">
        <div className="bridge-total-label">
          Forecast
        </div>

        <div className="bridge-total-value">
          {formatCurrency(
            forecast.forecast.forecast_revenue
          )}
        </div>
      </div>
    </div>
  );
}

/* ============================================================
   MONTE CARLO DISTRIBUTION
============================================================ */

function ForecastDistribution({
  intelligence,
}: {
  intelligence: IntelligenceOverview;
}) {
  const distribution =
    intelligence.monte_carlo.distribution;

  const values = [
    {
      label: "P10",
      value: distribution.p10,
    },
    {
      label: "P25",
      value: distribution.p25,
    },
    {
      label: "P50",
      value: distribution.p50,
    },
    {
      label: "P75",
      value: distribution.p75,
    },
    {
      label: "P90",
      value: distribution.p90,
    },
  ];

  const min = distribution.p10;
  const max = distribution.p90;
  const range = max - min || 1;

  return (
    <div className="distribution">
      <div className="distribution-scale">
        {values.map((item) => {
          const position =
            ((item.value - min) / range) * 100;

          return (
            <div
              className="distribution-point"
              key={item.label}
              style={{
                left: `${position}%`,
              }}
            >
              <div className="distribution-value">
                {formatCurrency(item.value)}
              </div>

              <div className="distribution-marker" />

              <div className="distribution-label">
                {item.label}
              </div>
            </div>
          );
        })}
      </div>

      <div className="distribution-line">
        <div className="distribution-range" />
      </div>

      <div className="distribution-caption">
        <span>Lower outcome</span>
        <span>Higher outcome</span>
      </div>
    </div>
  );
}

/* ============================================================
   PAGE
============================================================ */

export default function ForecastPage() {
  const [forecast, setForecast] =
    useState<ForecastCurrentResponse | null>(null);

  const [variance, setVariance] =
    useState<VarianceResponse | null>(null);

  const [intelligence, setIntelligence] =
    useState<IntelligenceOverview | null>(null);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState<string | null>(null);

  /* ----------------------------------------------------------
     LOAD
  ---------------------------------------------------------- */

  useEffect(() => {
    async function loadForecast() {
      try {
        setLoading(true);
        setError(null);

        const [
          forecastData,
          varianceData,
          intelligenceData,
        ] = await Promise.all([
          getForecast(),
          getVariance(),
          getIntelligence(),
        ]);

        setForecast(forecastData);
        setVariance(varianceData);
        setIntelligence(intelligenceData);
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Unable to load forecast data."
        );
      } finally {
        setLoading(false);
      }
    }

    loadForecast();
  }, []);

  /* ----------------------------------------------------------
     DERIVED METRICS
  ---------------------------------------------------------- */

  const metrics = useMemo(() => {
    if (!forecast || !variance) {
      return null;
    }

    const forecastValue =
      forecast.forecast.forecast_revenue;

    const budget = variance.budget;

    const varianceValue =
      forecastValue - budget;

    const variancePct =
      budget !== 0
        ? (varianceValue / budget) * 100
        : 0;

    const pipelineDependency =
      forecastValue !== 0
        ? (forecast.forecast.weighted_pipeline /
            forecastValue) *
          100
        : 0;

    const committedCoverage =
      forecastValue !== 0
        ? (forecast.forecast.committed_backlog /
            forecastValue) *
          100
        : 0;

    return {
      forecastValue,
      budget,
      varianceValue,
      variancePct,
      pipelineDependency,
      committedCoverage,
    };
  }, [forecast, variance]);

  /* ----------------------------------------------------------
     LOADING
  ---------------------------------------------------------- */

  if (loading) {
    return (
      <main className="app-shell">
        <div className="loading-screen">
          <div className="loading-mark">
            X
          </div>

          <div>
            <div className="loading-title">
              X-Fin
            </div>

            <div className="loading-subtitle">
              Loading forecast data
            </div>
          </div>
        </div>
      </main>
    );
  }

  /* ----------------------------------------------------------
     ERROR
  ---------------------------------------------------------- */

  if (error) {
    return (
      <main className="app-shell">
        <div className="error-screen">
          <div className="eyebrow">
            FORECAST
          </div>

          <h1>
            Unable to load forecast
          </h1>

          <p>{error}</p>

          <button
            className="secondary-button"
            onClick={() =>
              window.location.reload()
            }
          >
            Retry
          </button>
        </div>
      </main>
    );
  }

  if (
    !forecast ||
    !variance ||
    !intelligence ||
    !metrics
  ) {
    return null;
  }

  /* ----------------------------------------------------------
     RENDER
  ---------------------------------------------------------- */

  return (
    <main className="app-shell">
      {/* ======================================================
          SIDEBAR
      ====================================================== */}

      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">
            X
          </div>

          <div>
            <div className="brand-name">
              X-Fin
            </div>

            <div className="brand-caption">
              Delivery Finance
            </div>
          </div>
        </div>

        <nav className="navigation">
          <div className="nav-group">
            <div className="nav-heading">
              Workspace
            </div>

            <a
              className="nav-item"
              href="/"
            >
              Overview
            </a>

            <a
              className="nav-item"
              href="/financials"
            >
              Financials
            </a>

            <a
              className="nav-item active"
              href="/forecast"
            >
              Forecast
            </a>

            <a
              className="nav-item"
              href="/pipeline"
            >
              Pipeline
            </a>

            <a
              className="nav-item"
              href="/operations"
            >
              Operations
            </a>
          </div>

          <div className="nav-group">
            <div className="nav-heading">
              Analysis
            </div>

            <a
              className="nav-item"
              href="/scenarios"
            >
              Scenarios
            </a>
          </div>
        </nav>

        <div className="sidebar-footer">
          <div className="status-label">
            Data status
          </div>

          <div className="status-row">
            <span className="status-dot" />

            <span>
              Connected
            </span>
          </div>

          <div className="status-detail">
            Finance data current
          </div>
        </div>
      </aside>

      {/* ======================================================
          MAIN CONTENT
      ====================================================== */}

      <section className="main-content">
        <header className="topbar">
          <div>
            <div className="eyebrow">
              DELIVERY FINANCE
            </div>

            <h1>
              Forecast
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
              PRIMARY FORECAST METRICS
          ================================================== */}

          <section className="metric-grid">
            <div className="metric-block">
              <div className="metric-label">
                Current forecast
              </div>

              <div className="metric-value">
                {formatCurrency(
                  metrics.forecastValue
                )}
              </div>

              <div
                className={`metric-change ${
                  metrics.variancePct >= 0
                    ? "positive"
                    : "negative"
                }`}
              >
                {formatPercent(
                  metrics.variancePct
                )}

                <span>
                  vs budget
                </span>
              </div>
            </div>

            <div className="metric-block">
              <div className="metric-label">
                Budget
              </div>

              <div className="metric-value">
                {formatCurrency(
                  metrics.budget
                )}
              </div>

              <div className="metric-secondary">
                Revenue target
              </div>
            </div>

            <div className="metric-block">
              <div className="metric-label">
                Forecast variance
              </div>

              <div
                className={`metric-value ${
                  metrics.varianceValue >= 0
                    ? "value-positive"
                    : "value-negative"
                }`}
              >
                {metrics.varianceValue >= 0
                  ? "+"
                  : "−"}

                {formatCurrency(
                  Math.abs(
                    metrics.varianceValue
                  )
                )}
              </div>

              <div className="metric-secondary">
                Forecast less budget
              </div>
            </div>

            <div className="metric-block">
              <div className="metric-label">
                Pipeline dependency
              </div>

              <div className="metric-value">
                {formatPlainPercent(
                  metrics.pipelineDependency
                )}
              </div>

              <div className="metric-secondary">
                Weighted pipeline / forecast
              </div>
            </div>
          </section>

          {/* ==================================================
              FORECAST CONSTRUCTION
          ================================================== */}

          <section className="section">
            <div className="section-header">
              <div>
                <div className="section-kicker">
                  FORECAST CONSTRUCTION
                </div>

                <h2>
                  Forecast bridge
                </h2>
              </div>

              <div className="section-meta">
                Current operating forecast
              </div>
            </div>

            <div className="panel forecast-panel">
              <ForecastBridge
                forecast={forecast}
              />
            </div>
          </section>

          {/* ==================================================
              ASSUMPTIONS
          ================================================== */}

          <section className="section">
            <div className="section-header">
              <div>
                <div className="section-kicker">
                  ASSUMPTIONS
                </div>

                <h2>
                  Forecast assumptions
                </h2>
              </div>
            </div>

            <div className="assumptions-grid">
              <div className="panel assumption-panel">
                <div className="panel-label">
                  Current utilization
                </div>

                <div className="panel-value">
                  {forecast.assumptions
                    ?.current_utilization !=
                  null
                    ? formatPlainPercent(
                        forecast.assumptions
                          .current_utilization *
                          100
                      )
                    : "Not measured"}
                </div>

                <div className="assumption-note">
                  Current operating level
                </div>
              </div>

              <div className="panel assumption-panel">
                <div className="panel-label">
                  Target utilization
                </div>

                <div className="panel-value">
                  {forecast.assumptions
                    ?.target_utilization !=
                  null
                    ? formatPlainPercent(
                        forecast.assumptions
                          .target_utilization *
                          100
                      )
                    : "Not available"}
                </div>

                <div className="assumption-note">
                  Forecast engine assumption
                </div>
              </div>

              <div className="panel assumption-panel">
                <div className="panel-label">
                  Execution risk
                </div>

                <div className="panel-value">
                  {forecast.assumptions
                    ?.execution_risk_rate !=
                  null
                    ? formatPlainPercent(
                        forecast.assumptions
                          .execution_risk_rate *
                          100
                      )
                    : "Not available"}
                </div>

                <div className="assumption-note">
                  Applied to forward revenue
                </div>
              </div>

              <div className="panel assumption-panel">
                <div className="panel-label">
                  Committed coverage
                </div>

                <div className="panel-value">
                  {formatPlainPercent(
                    metrics.committedCoverage
                  )}
                </div>

                <div className="assumption-note">
                  Backlog / forecast
                </div>
              </div>
            </div>
          </section>

          {/* ==================================================
              FORWARD POSITION
          ================================================== */}

          <section className="section">
            <div className="section-header">
              <div>
                <div className="section-kicker">
                  FORWARD POSITION
                </div>

                <h2>
                  Revenue support
                </h2>
              </div>
            </div>

            <div className="position-grid">
              <div className="panel position-panel">
                <div className="panel-label">
                  Committed backlog
                </div>

                <div className="panel-value">
                  {formatCurrency(
                    forecast.backlog
                      .committed_backlog
                  )}
                </div>

                <div className="panel-note">
                  Contracted revenue
                </div>
              </div>

              <div className="panel position-panel">
                <div className="panel-label">
                  Weighted pipeline
                </div>

                <div className="panel-value">
                  {formatCurrency(
                    forecast.pipeline
                      .weighted_pipeline
                  )}
                </div>

                <div className="panel-note">
                  Probability-weighted
                  opportunities
                </div>
              </div>

              <div className="panel position-panel">
                <div className="panel-label">
                  Total coverage
                </div>

                <div className="panel-value">
                  {formatCurrency(
                    forecast.backlog
                      .total_coverage
                  )}
                </div>

                <div className="panel-note">
                  Backlog + uncommitted
                  pipeline
                </div>
              </div>

              <div className="panel position-panel">
                <div className="panel-label">
                  Opportunities
                </div>

                <div className="panel-value">
                  {forecast.pipeline.opportunities.toLocaleString(
                    "en-IN"
                  )}
                </div>

                <div className="panel-note">
                  Pipeline opportunities
                </div>
              </div>
            </div>
          </section>

          {/* ==================================================
              MONTE CARLO DISTRIBUTION
          ================================================== */}

          <section className="section">
            <div className="section-header">
              <div>
                <div className="section-kicker">
                  DISTRIBUTION
                </div>

                <h2>
                  Forecast range
                </h2>
              </div>

              <div className="section-meta">
                {intelligence.monte_carlo.iterations.toLocaleString(
                  "en-IN"
                )}{" "}
                iterations
              </div>
            </div>

            <div className="panel distribution-panel">
              <ForecastDistribution
                intelligence={intelligence}
              />

              <div className="distribution-summary">
                <div>
                  <span className="summary-label">
                    Mean
                  </span>

                  <strong>
                    {formatCurrency(
                      intelligence
                        .monte_carlo
                        .distribution
                        .mean
                    )}
                  </strong>
                </div>

                <div>
                  <span className="summary-label">
                    Standard deviation
                  </span>

                  <strong>
                    {formatCurrency(
                      intelligence
                        .monte_carlo
                        .distribution
                        .standard_deviation
                    )}
                  </strong>
                </div>

                <div>
                  <span className="summary-label">
                    P10–P90 range
                  </span>

                  <strong>
                    {formatCurrency(
                      intelligence
                        .monte_carlo
                        .distribution
                        .range_p10_p90
                    )}
                  </strong>
                </div>
              </div>

              <div className="assumption-note">
                Probabilistic distribution is shown
                separately from the deterministic
                operating forecast above.
              </div>
            </div>
          </section>

          {/* ==================================================
              BUDGET ANALYSIS
          ================================================== */}

          <section className="section">
            <div className="section-header">
              <div>
                <div className="section-kicker">
                  BUDGET ANALYSIS
                </div>

                <h2>
                  Distribution relative to budget
                </h2>
              </div>
            </div>

            <div className="analysis-grid">
              <div className="panel analysis-panel">
                <div className="panel-label">
                  Probability above budget
                </div>

                <div className="analysis-value positive">
                  {formatPlainPercent(
                    intelligence
                      .monte_carlo
                      .budget_analysis
                      .probability_above_budget
                  )}
                </div>

                <div className="analysis-note">
                  Monte Carlo estimate
                </div>
              </div>

              <div className="panel analysis-panel">
                <div className="panel-label">
                  Probability below budget
                </div>

                <div className="analysis-value negative">
                  {formatPlainPercent(
                    intelligence
                      .monte_carlo
                      .budget_analysis
                      .probability_below_budget
                  )}
                </div>

                <div className="analysis-note">
                  Monte Carlo estimate
                </div>
              </div>

              <div className="panel analysis-panel">
                <div className="panel-label">
                  P50 vs budget
                </div>

                <div className="analysis-value">
                  {formatCurrency(
                    intelligence
                      .monte_carlo
                      .budget_analysis
                      .p50_vs_budget
                  )}
                </div>

                <div className="analysis-note">
                  Median forecast variance
                </div>
              </div>

              <div className="panel analysis-panel">
                <div className="panel-label">
                  Downside at P10
                </div>

                <div className="analysis-value">
                  {formatCurrency(
                    intelligence
                      .monte_carlo
                      .risk
                      .downside_at_p10
                  )}
                </div>

                <div className="analysis-note">
                  P10 downside
                </div>
              </div>
            </div>
          </section>

          {/* ==================================================
              FORECAST CONTEXT
          ================================================== */}

          <section className="section">
            <div className="section-header">
              <div>
                <div className="section-kicker">
                  CONTEXT
                </div>

                <h2>
                  Forecast position
                </h2>
              </div>
            </div>

            <div className="context-table panel">
              <div className="context-row context-header">
                <span>
                  Measure
                </span>

                <span>
                  Value
                </span>

                <span>
                  Interpretation
                </span>
              </div>

              <div className="context-row">
                <span>
                  Forecast variance
                </span>

                <strong>
                  {formatCurrency(
                    metrics.varianceValue
                  )}
                </strong>

                <span>
                  Deterministic forecast
                  relative to budget
                </span>
              </div>

              <div className="context-row">
                <span>
                  Pipeline dependency
                </span>

                <strong>
                  {formatPlainPercent(
                    metrics.pipelineDependency
                  )}
                </strong>

                <span>
                  Share of forecast represented
                  by weighted pipeline
                </span>
              </div>

              <div className="context-row">
                <span>
                  Execution risk adjustment
                </span>

                <strong>
                  {formatCurrency(
                    Math.abs(
                      forecast.forecast
                        .risk_adjustment
                    )
                  )}
                </strong>

                <span>
                  Reduction applied in the
                  operating forecast
                </span>
              </div>

              <div className="context-row">
                <span>
                  Model confidence indicator
                </span>

                <strong>
                  {formatPlainPercent(
                    intelligence.reasoning
                      .forecast_confidence_base
                  )}
                </strong>

                <span>
                  Base model indicator; not a
                  statistical confidence interval
                </span>
              </div>
            </div>
          </section>
        </div>
      </section>
    </main>
  );
}