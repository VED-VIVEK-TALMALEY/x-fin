"use client";

import { useEffect, useMemo, useState } from "react";
import Sidebar from "@/components/Sidebar";
import { getIntelligence } from "@/lib/api";

import type {
  IntelligenceOverview,
} from "@/types/intelligence";

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
  return new Intl.NumberFormat("en-IN").format(
    value
  );
}

function formatPercent(value: number) {
  return `${value.toFixed(1)}%`;
}

function formatRate(value: number) {
  return `₹${value.toLocaleString("en-IN", {
    maximumFractionDigits: 0,
  })}`;
}

/* ============================================================
   VALUE HELPERS
============================================================ */

function nullablePercent(
  value: number | null
) {
  if (value === null || !Number.isFinite(value)) {
    return "Not measured";
  }

  return formatPercent(value);
}

/* ============================================================
   HOURS BAR
============================================================ */

function HoursComparison({
  actual,
  budget,
}: {
  actual: number;
  budget: number;
}) {
  const maximum = Math.max(actual, budget, 1);

  const actualWidth =
    (actual / maximum) * 100;

  const budgetWidth =
    (budget / maximum) * 100;

  return (
    <div className="hours-comparison">
      <div className="hours-scale">
        <div className="hours-scale-label">
          <span>Budget</span>

          <strong>
            {formatNumber(budget)} hrs
          </strong>
        </div>

        <div className="hours-track">
          <div
            className="hours-budget"
            style={{
              width: `${budgetWidth}%`,
            }}
          />
        </div>
      </div>

      <div className="hours-scale">
        <div className="hours-scale-label">
          <span>Actual</span>

          <strong>
            {formatNumber(actual)} hrs
          </strong>
        </div>

        <div className="hours-track">
          <div
            className="hours-actual"
            style={{
              width: `${actualWidth}%`,
            }}
          />
        </div>
      </div>
    </div>
  );
}

/* ============================================================
   PAGE
============================================================ */

export default function OperationsPage() {
  const [data, setData] =
    useState<IntelligenceOverview | null>(
      null
    );

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState<string | null>(null);

  /* ----------------------------------------------------------
     LOAD
  ---------------------------------------------------------- */

  useEffect(() => {
    async function loadOperations() {
      try {
        setLoading(true);
        setError(null);

        const response =
          await getIntelligence();

        setData(response);
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Unable to load operations data."
        );
      } finally {
        setLoading(false);
      }
    }

    loadOperations();
  }, []);

  /* ----------------------------------------------------------
     DERIVED METRICS
  ---------------------------------------------------------- */

  const metrics = useMemo(() => {
    if (!data) {
      return null;
    }

    const staffing = data.staffing;

    const hoursVariance =
      staffing.actual_hours -
      staffing.budget_hours;

    const hoursVariancePct =
      staffing.budget_hours !== 0
        ? (hoursVariance /
            staffing.budget_hours) *
          100
        : 0;

    const costVariance =
      staffing.actual_cost -
      data.source_metrics.actual_cost;

    return {
      hoursVariance,
      hoursVariancePct,
      costVariance,
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
                Loading operations data
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
              OPERATIONS
            </div>

            <h1>
              Unable to load operations data
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

  const staffing = data.staffing;

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
              Operations
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
                Actual hours
              </div>

              <div className="metric-value">
                {formatNumber(
                  staffing.actual_hours
                )}
              </div>

              <div className="metric-secondary">
                Delivery hours recorded
              </div>
            </div>

            <div className="metric-block">
              <div className="metric-label">
                Budget hours
              </div>

              <div className="metric-value">
                {formatNumber(
                  staffing.budget_hours
                )}
              </div>

              <div className="metric-secondary">
                Planned delivery hours
              </div>
            </div>

            <div className="metric-block">
              <div className="metric-label">
                Hours attainment
              </div>

              <div className="metric-value">
                {formatPercent(
                  staffing.hours_attainment_pct
                )}
              </div>

              <div className="metric-secondary">
                Actual hours / budget hours
              </div>
            </div>

            <div className="metric-block">
              <div className="metric-label">
                Actual delivery cost
              </div>

              <div className="metric-value">
                {formatCurrency(
                  staffing.actual_cost
                )}
              </div>

              <div className="metric-secondary">
                Recorded delivery cost
              </div>
            </div>
          </section>

          {/* ==================================================
              HOURS PERFORMANCE
          ================================================== */}

          <section className="section">
            <div className="section-header">
              <div>
                <div className="section-kicker">
                  DELIVERY HOURS
                </div>

                <h2>
                  Hours performance
                </h2>
              </div>

              <div className="section-meta">
                Actual against budget
              </div>
            </div>

            <div className="panel operations-hours-panel">
              <div className="operations-summary">
                <div>
                  <div className="panel-label">
                    Hours variance
                  </div>

                  <div className="operations-primary-value">
                    {metrics.hoursVariance >= 0
                      ? "+"
                      : "−"}

                    {formatNumber(
                      Math.abs(
                        metrics.hoursVariance
                      )
                    )}{" "}
                    hrs
                  </div>
                </div>

                <div className="operations-summary-side">
                  <span>
                    Variance
                  </span>

                  <strong>
                    {metrics.hoursVariancePct >=
                    0
                      ? "+"
                      : "−"}

                    {formatPercent(
                      Math.abs(
                        metrics.hoursVariancePct
                      )
                    )}
                  </strong>
                </div>
              </div>

              <HoursComparison
                actual={
                  staffing.actual_hours
                }
                budget={
                  staffing.budget_hours
                }
              />
            </div>
          </section>

          {/* ==================================================
              COST AND PRODUCTIVITY
          ================================================== */}

          <section className="section">
            <div className="section-header">
              <div>
                <div className="section-kicker">
                  DELIVERY ECONOMICS
                </div>

                <h2>
                  Cost and productivity
                </h2>
              </div>

              <div className="section-meta">
                Current delivery period
              </div>
            </div>

            <div className="operations-detail-grid">
              <div className="panel operations-detail">
                <div className="panel-label">
                  Actual cost
                </div>

                <div className="panel-value">
                  {formatCurrency(
                    staffing.actual_cost
                  )}
                </div>

                <div className="panel-note">
                  Total recorded delivery cost
                </div>
              </div>

              <div className="panel operations-detail">
                <div className="panel-label">
                  Cost per hour
                </div>

                <div className="panel-value">
                  {formatRate(
                    staffing.blended_cost_per_hour
                  )}
                </div>

                <div className="panel-note">
                  Blended delivery cost
                </div>
              </div>

              <div className="panel operations-detail">
                <div className="panel-label">
                  Revenue per hour
                </div>

                <div className="panel-value">
                  {formatRate(
                    staffing.realized_revenue_per_hour
                  )}
                </div>

                <div className="panel-note">
                  Realized revenue / actual hours
                </div>
              </div>

              <div className="panel operations-detail">
                <div className="panel-label">
                  Gross contribution
                </div>

                <div className="panel-value">
                  {formatCurrency(
                    staffing.actual_revenue -
                      staffing.actual_cost
                  )}
                </div>

                <div className="panel-note">
                  Revenue less delivery cost
                </div>
              </div>
            </div>
          </section>

          {/* ==================================================
              CAPACITY
          ================================================== */}

          <section className="section">
            <div className="section-header">
              <div>
                <div className="section-kicker">
                  CAPACITY
                </div>

                <h2>
                  Utilization and capacity
                </h2>
              </div>

              <div className="section-meta">
                Data availability shown explicitly
              </div>
            </div>

            <div className="panel capacity-panel">
              <div className="capacity-grid">
                <div className="capacity-item">
                  <span>
                    Actual utilization
                  </span>

                  <strong>
                    {nullablePercent(
                      staffing.actual_utilization
                    )}
                  </strong>
                </div>

                <div className="capacity-item">
                  <span>
                    Budget utilization
                  </span>

                  <strong>
                    {formatPercent(
                      staffing.budget_utilization
                    )}
                  </strong>
                </div>

                <div className="capacity-item">
                  <span>
                    Utilization gap
                  </span>

                  <strong>
                    {nullablePercent(
                      staffing.utilization_gap
                    )}
                  </strong>
                </div>

                <div className="capacity-item">
                  <span>
                    Bench hours
                  </span>

                  <strong>
                    {staffing.bench_hours ===
                    null
                      ? "Not measured"
                      : `${formatNumber(
                          staffing.bench_hours
                        )} hrs`}
                  </strong>
                </div>
              </div>

              <div className="capacity-note">
                <div className="capacity-note-title">
                  Measurement note
                </div>

                <p>
                  {staffing.capacity_measurement_note}
                </p>
              </div>
            </div>
          </section>

          {/* ==================================================
              STAFFING POSITION
          ================================================== */}

          <section className="section">
            <div className="section-header">
              <div>
                <div className="section-kicker">
                  STAFFING POSITION
                </div>

                <h2>
                  Capacity indicators
                </h2>
              </div>
            </div>

            <div className="operations-detail-grid">
              <div className="panel operations-detail">
                <div className="panel-label">
                  Capacity status
                </div>

                <div className="status-value">
                  {staffing.capacity_status}
                </div>

                <div className="panel-note">
                  Current staffing position
                </div>
              </div>

              <div className="panel operations-detail">
                <div className="panel-label">
                  Bench risk
                </div>

                <div className="status-value">
                  {staffing.bench_risk}
                </div>

                <div className="panel-note">
                  Based on available capacity data
                </div>
              </div>

              <div className="panel operations-detail">
                <div className="panel-label">
                  Bench percentage
                </div>

                <div className="panel-value">
                  {staffing.bench_percentage ===
                  null
                    ? "Not measured"
                    : formatPercent(
                        staffing.bench_percentage
                      )}
                </div>

                <div className="panel-note">
                  Share of available capacity
                </div>
              </div>

              <div className="panel operations-detail">
                <div className="panel-label">
                  Estimated bench cost
                </div>

                <div className="panel-value">
                  {staffing.estimated_bench_cost ===
                  null
                    ? "Not measured"
                    : formatCurrency(
                        staffing.estimated_bench_cost
                      )}
                </div>

                <div className="panel-note">
                  Derived only where capacity data permits
                </div>
              </div>
            </div>
          </section>

          {/* ==================================================
              DATA QUALITY
          ================================================== */}

          <section className="section">
            <div className="section-header">
              <div>
                <div className="section-kicker">
                  DATA QUALITY
                </div>

                <h2>
                  Operations data status
                </h2>
              </div>

              <div className="section-meta">
                Source measurement
              </div>
            </div>

            <div className="panel data-quality-panel">
              <div className="data-quality-header">
                <span>
                  Utilization measurement
                </span>

                <strong>
                  {staffing.utilization_data_quality}
                </strong>
              </div>

              <p>
                {staffing.capacity_measurement_note}
              </p>
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
                  Actual delivery hours are{" "}
                  <strong>
                    {formatPercent(
                      staffing.hours_attainment_pct
                    )}
                  </strong>{" "}
                  of budgeted hours, representing
                  a variance of{" "}
                  <strong>
                    {metrics.hoursVariance >=
                    0
                      ? "+"
                      : "−"}

                    {formatNumber(
                      Math.abs(
                        metrics.hoursVariance
                      )
                    )}{" "}
                    hours
                  </strong>
                  .
                </p>
              </div>

              <div className="observation">
                <span className="observation-index">
                  02
                </span>

                <p>
                  Recorded delivery cost is{" "}
                  <strong>
                    {formatCurrency(
                      staffing.actual_cost
                    )}
                  </strong>
                  , with a blended cost of{" "}
                  <strong>
                    {formatRate(
                      staffing.blended_cost_per_hour
                    )}
                  </strong>{" "}
                  per hour.
                </p>
              </div>

              <div className="observation">
                <span className="observation-index">
                  03
                </span>

                <p>
                  Realized revenue per delivery
                  hour is{" "}
                  <strong>
                    {formatRate(
                      staffing.realized_revenue_per_hour
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
                  Actual utilization is shown as{" "}
                  <strong>
                    {nullablePercent(
                      staffing.actual_utilization
                    )}
                  </strong>{" "}
                  because the current source data
                  does not provide the required
                  capacity denominator.
                </p>
              </div>
            </div>
          </section>
        </div>
      </section>
    </main>
  );
}