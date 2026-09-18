"use client";

import { useEffect, useMemo, useState } from "react";

import Sidebar from "@/components/Sidebar";

import { getForecast } from "@/lib/api";

import type { ForecastCurrentResponse } from "@/types/forecast";

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

function formatNumber(value: number) {
  return new Intl.NumberFormat("en-IN").format(value);
}

function formatPercent(value: number) {
  return `${value.toFixed(1)}%`;
}

/* ============================================================
   COVERAGE BAR
============================================================ */

function CoverageBar({
  committed,
  weightedPipeline,
  forecast,
}: {
  committed: number;
  weightedPipeline: number;
  forecast: number;
}) {
  const total =
    committed + weightedPipeline;

  const committedWidth =
    total > 0
      ? (committed / total) * 100
      : 0;

  const pipelineWidth =
    total > 0
      ? (weightedPipeline / total) * 100
      : 0;

  const forecastPosition =
    total > 0
      ? Math.min(
          (forecast / total) * 100,
          100
        )
      : 0;

  return (
    <div className="coverage-visual">
      <div className="coverage-track">
        <div
          className="coverage-committed"
          style={{
            width: `${committedWidth}%`,
          }}
        />

        <div
          className="coverage-pipeline"
          style={{
            width: `${pipelineWidth}%`,
          }}
        />

        <div
          className="coverage-marker"
          style={{
            left: `${forecastPosition}%`,
          }}
        />
      </div>

      <div className="coverage-legend">
        <div className="coverage-legend-item">
          <span className="legend-dot committed" />
          <span>
            Committed backlog
          </span>
        </div>

        <div className="coverage-legend-item">
          <span className="legend-dot pipeline" />
          <span>
            Weighted pipeline
          </span>
        </div>

        <div className="coverage-legend-item">
          <span className="legend-marker" />
          <span>
            Forecast
          </span>
        </div>
      </div>
    </div>
  );
}

/* ============================================================
   PIPELINE COMPOSITION
============================================================ */

function PipelineComposition({
  committed,
  uncommitted,
}: {
  committed: number;
  uncommitted: number;
}) {
  const total =
    committed + uncommitted;

  const committedPercentage =
    total > 0
      ? (committed / total) * 100
      : 0;

  const uncommittedPercentage =
    total > 0
      ? (uncommitted / total) * 100
      : 0;

  return (
    <div className="composition">
      <div className="composition-track">
        <div
          className="composition-committed"
          style={{
            width: `${committedPercentage}%`,
          }}
        />

        <div
          className="composition-uncommitted"
          style={{
            width: `${uncommittedPercentage}%`,
          }}
        />
      </div>

      <div className="composition-labels">
        <div>
          <span className="composition-name">
            Committed backlog
          </span>

          <strong>
            {formatCurrency(committed)}
          </strong>
        </div>

        <div>
          <span className="composition-name">
            Uncommitted pipeline
          </span>

          <strong>
            {formatCurrency(uncommitted)}
          </strong>
        </div>
      </div>
    </div>
  );
}

/* ============================================================
   PAGE
============================================================ */

export default function PipelinePage() {
  const [data, setData] =
    useState<ForecastCurrentResponse | null>(
      null
    );

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState<string | null>(null);

  /* ----------------------------------------------------------
     LOAD DATA
  ---------------------------------------------------------- */

  useEffect(() => {
    async function loadPipeline() {
      try {
        setLoading(true);
        setError(null);

        const response =
          await getForecast();

        setData(response);
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Unable to load pipeline data."
        );
      } finally {
        setLoading(false);
      }
    }

    loadPipeline();
  }, []);

  /* ----------------------------------------------------------
     DERIVED VALUES
  ---------------------------------------------------------- */

  const metrics = useMemo(() => {
    if (!data) {
      return null;
    }

    const {
      pipeline,
      backlog,
      forecast,
    } = data;

    const weightedPipelineShare =
      forecast.forecast_revenue > 0
        ? (pipeline.weighted_pipeline /
            forecast.forecast_revenue) *
          100
        : 0;

    const committedShare =
      backlog.total_coverage > 0
        ? (backlog.committed_backlog /
            backlog.total_coverage) *
          100
        : 0;

    const uncommittedShare =
      backlog.total_coverage > 0
        ? (backlog.uncommitted_pipeline /
            backlog.total_coverage) *
          100
        : 0;

    const coverageToForecast =
      forecast.forecast_revenue > 0
        ? (backlog.total_coverage /
            forecast.forecast_revenue) *
          100
        : 0;

    const grossPipelineToForecast =
      forecast.forecast_revenue > 0
        ? (pipeline.pipeline_value /
            forecast.forecast_revenue) *
          100
        : 0;

    return {
      weightedPipelineShare,
      committedShare,
      uncommittedShare,
      coverageToForecast,
      grossPipelineToForecast,
    };
  }, [data]);

  /* ----------------------------------------------------------
     LOADING
  ---------------------------------------------------------- */

  if (loading) {
    return (
      <main className="app-shell">
        <Sidebar />

        <section className="main-content">
          <div className="loading-screen">
            <div className="loading-mark">
              X
            </div>

            <div>
              <div className="loading-title">
                X-Fin
              </div>

              <div className="loading-subtitle">
                Loading pipeline data
              </div>
            </div>
          </div>
        </section>
      </main>
    );
  }

  /* ----------------------------------------------------------
     ERROR
  ---------------------------------------------------------- */

  if (error) {
    return (
      <main className="app-shell">
        <Sidebar />

        <section className="main-content">
          <div className="error-screen">
            <div className="eyebrow">
              PIPELINE
            </div>

            <h1>
              Unable to load pipeline data
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
        </section>
      </main>
    );
  }

  if (!data || !metrics) {
    return null;
  }

  const {
    forecast,
    pipeline,
    backlog,
  } = data;

  /* ----------------------------------------------------------
     RENDER
  ---------------------------------------------------------- */

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
              Pipeline
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
              KPI ROW
          ================================================== */}

          <section className="metric-grid">
            <div className="metric-block">
              <div className="metric-label">
                Pipeline value
              </div>

              <div className="metric-value">
                {formatCurrency(
                  pipeline.pipeline_value
                )}
              </div>

              <div className="metric-secondary">
                {formatNumber(
                  pipeline.opportunities
                )}{" "}
                opportunities
              </div>
            </div>

            <div className="metric-block">
              <div className="metric-label">
                Weighted pipeline
              </div>

              <div className="metric-value">
                {formatCurrency(
                  pipeline.weighted_pipeline
                )}
              </div>

              <div className="metric-secondary">
                Probability-weighted value
              </div>
            </div>

            <div className="metric-block">
              <div className="metric-label">
                Committed backlog
              </div>

              <div className="metric-value">
                {formatCurrency(
                  backlog.committed_backlog
                )}
              </div>

              <div className="metric-secondary">
                Contracted revenue
              </div>
            </div>

            <div className="metric-block">
              <div className="metric-label">
                Total coverage
              </div>

              <div className="metric-value">
                {formatCurrency(
                  backlog.total_coverage
                )}
              </div>

              <div className="metric-secondary">
                Committed backlog + uncommitted pipeline
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
                  Revenue coverage
                </h2>
              </div>

              <div className="section-meta">
                Current forecast position
              </div>
            </div>

            <div className="panel pipeline-coverage-panel">
              <div className="coverage-summary">
                <div>
                  <div className="panel-label">
                    Forecast revenue
                  </div>

                  <div className="coverage-value">
                    {formatCurrency(
                      forecast.forecast_revenue
                    )}
                  </div>
                </div>

                <div className="coverage-side-metric">
                  <span>
                    Total coverage
                  </span>

                  <strong>
                    {formatCurrency(
                      backlog.total_coverage
                    )}
                  </strong>
                </div>
              </div>

              <CoverageBar
                committed={
                  backlog.committed_backlog
                }
                weightedPipeline={
                  pipeline.weighted_pipeline
                }
                forecast={
                  forecast.forecast_revenue
                }
              />

              <div className="coverage-detail">
                <span>
                  Coverage / forecast
                </span>

                <strong>
                  {formatPercent(
                    metrics.coverageToForecast
                  )}
                </strong>
              </div>
            </div>
          </section>

          {/* ==================================================
              PIPELINE COMPOSITION
          ================================================== */}

          <section className="section">
            <div className="section-header">
              <div>
                <div className="section-kicker">
                  PIPELINE COMPOSITION
                </div>

                <h2>
                  Committed and uncommitted revenue
                </h2>
              </div>

              <div className="section-meta">
                Forward coverage
              </div>
            </div>

            <div className="panel composition-panel">
              <PipelineComposition
                committed={
                  backlog.committed_backlog
                }
                uncommitted={
                  backlog.uncommitted_pipeline
                }
              />

              <div className="composition-details">
                <div className="composition-detail">
                  <span>
                    Committed share
                  </span>

                  <strong>
                    {formatPercent(
                      metrics.committedShare
                    )}
                  </strong>
                </div>

                <div className="composition-detail">
                  <span>
                    Uncommitted share
                  </span>

                  <strong>
                    {formatPercent(
                      metrics.uncommittedShare
                    )}
                  </strong>
                </div>

                <div className="composition-detail">
                  <span>
                    Weighted pipeline / forecast
                  </span>

                  <strong>
                    {formatPercent(
                      metrics.weightedPipelineShare
                    )}
                  </strong>
                </div>
              </div>
            </div>
          </section>

          {/* ==================================================
              PIPELINE METRICS
          ================================================== */}

          <section className="section">
            <div className="section-header">
              <div>
                <div className="section-kicker">
                  PIPELINE METRICS
                </div>

                <h2>
                  Pipeline detail
                </h2>
              </div>
            </div>

            <div className="pipeline-detail-grid">
              <div className="panel pipeline-detail">
                <div className="panel-label">
                  Gross pipeline
                </div>

                <div className="panel-value">
                  {formatCurrency(
                    pipeline.pipeline_value
                  )}
                </div>

                <div className="panel-note">
                  Total opportunity value
                </div>
              </div>

              <div className="panel pipeline-detail">
                <div className="panel-label">
                  Weighted pipeline
                </div>

                <div className="panel-value">
                  {formatCurrency(
                    pipeline.weighted_pipeline
                  )}
                </div>

                <div className="panel-note">
                  Probability-weighted opportunity value
                </div>
              </div>

              <div className="panel pipeline-detail">
                <div className="panel-label">
                  Uncommitted pipeline
                </div>

                <div className="panel-value">
                  {formatCurrency(
                    backlog.uncommitted_pipeline
                  )}
                </div>

                <div className="panel-note">
                  Pipeline outside committed backlog
                </div>
              </div>

              <div className="panel pipeline-detail">
                <div className="panel-label">
                  Opportunities
                </div>

                <div className="panel-value">
                  {formatNumber(
                    pipeline.opportunities
                  )}
                </div>

                <div className="panel-note">
                  Current pipeline opportunities
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
                  Forward revenue construction
                </h2>
              </div>

              <div className="section-meta">
                Deterministic operating forecast
              </div>
            </div>

            <div className="panel bridge-panel">
              <div className="bridge-row">
                <span>
                  Committed backlog
                </span>

                <strong>
                  {formatCurrency(
                    forecast.committed_backlog
                  )}
                </strong>
              </div>

              <div className="bridge-row">
                <span>
                  Weighted pipeline
                </span>

                <strong>
                  {formatCurrency(
                    forecast.weighted_pipeline
                  )}
                </strong>
              </div>

              <div className="bridge-row adjustment">
                <span>
                  Utilization adjustment
                </span>

                <strong>
                  {forecast.utilization_adjustment >=
                  0
                    ? "+"
                    : "−"}

                  {formatCurrency(
                    Math.abs(
                      forecast.utilization_adjustment
                    )
                  )}
                </strong>
              </div>

              <div className="bridge-row adjustment">
                <span>
                  Execution risk
                </span>

                <strong>
                  −
                  {formatCurrency(
                    Math.abs(
                      forecast.risk_adjustment
                    )
                  )}
                </strong>
              </div>

              <div className="bridge-total">
                <span>
                  Forecast revenue
                </span>

                <strong>
                  {formatCurrency(
                    forecast.forecast_revenue
                  )}
                </strong>
              </div>
            </div>
          </section>

          {/* ==================================================
              KEY OBSERVATIONS
          ================================================== */}

          <section className="section last-section">
            <div className="section-header">
              <div>
                <div className="section-kicker">
                  ANALYSIS
                </div>

                <h2>
                  Key observations
                </h2>
              </div>
            </div>

            <div className="observations">
              <div className="observation">
                <span className="observation-index">
                  01
                </span>

                <p>
                  The current forward position
                  contains{" "}
                  <strong>
                    {formatCurrency(
                      backlog.committed_backlog
                    )}
                  </strong>{" "}
                  of committed backlog and{" "}
                  <strong>
                    {formatCurrency(
                      pipeline.weighted_pipeline
                    )}
                  </strong>{" "}
                  of probability-weighted
                  pipeline.
                </p>
              </div>

              <div className="observation">
                <span className="observation-index">
                  02
                </span>

                <p>
                  Gross pipeline of{" "}
                  <strong>
                    {formatCurrency(
                      pipeline.pipeline_value
                    )}
                  </strong>{" "}
                  is distributed across{" "}
                  <strong>
                    {formatNumber(
                      pipeline.opportunities
                    )}
                  </strong>{" "}
                  opportunities, with weighted
                  pipeline representing{" "}
                  <strong>
                    {formatPercent(
                      metrics.grossPipelineToForecast
                    )}
                  </strong>{" "}
                  of the current forecast on a
                  gross-value basis.
                </p>
              </div>

              <div className="observation">
                <span className="observation-index">
                  03
                </span>

                <p>
                  Total forward coverage is{" "}
                  <strong>
                    {formatCurrency(
                      backlog.total_coverage
                    )}
                  </strong>
                  , compared with a current
                  operating forecast of{" "}
                  <strong>
                    {formatCurrency(
                      forecast.forecast_revenue
                    )}
                  </strong>
                  .
                </p>
              </div>
            </div>
          </section>
        </div>
      </section>
    </main>
  );
}