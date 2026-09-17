"use client";

import { useEffect, useMemo, useState } from "react";

import Sidebar from "@/components/Sidebar";
import {
  getSummary,
  getVariance,
  getMonthlyRevenue,
  getBusinessUnits,
} from "@/lib/api";

import type {
  AnalyticsSummary,
  MonthlyRevenueResponse,
  VarianceResponse,
} from "@/types/analytics";

import type {
  BusinessUnitsResponse,
} from "@/types/business-units";

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
   SIMPLE COMPARISON BAR
============================================================ */

function RevenueComparison({
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
    <div className="financial-comparison">
      <div className="comparison-row">
        <div className="comparison-header">
          <span>Actual revenue</span>

          <strong>
            {formatCurrency(actual)}
          </strong>
        </div>

        <div className="comparison-track">
          <div
            className="comparison-bar actual"
            style={{
              width: `${actualWidth}%`,
            }}
          />
        </div>
      </div>

      <div className="comparison-row">
        <div className="comparison-header">
          <span>Budget revenue</span>

          <strong>
            {formatCurrency(budget)}
          </strong>
        </div>

        <div className="comparison-track">
          <div
            className="comparison-bar budget"
            style={{
              width: `${budgetWidth}%`,
            }}
          />
        </div>
      </div>

      <div className="comparison-footer">
        <span>
          Actual vs budget
        </span>

        <strong
          className={
            actual >= budget
              ? "value-positive"
              : "value-negative"
          }
        >
          {formatCurrency(
            actual - budget
          )}
        </strong>
      </div>
    </div>
  );
}

/* ============================================================
   MONTHLY REVENUE CHART
============================================================ */

function MonthlyRevenueChart({
  data,
}: {
  data: MonthlyRevenueResponse;
}) {
  const points = data.value ?? [];

  if (!points.length) {
    return (
      <div className="empty-chart">
        Revenue history unavailable.
      </div>
    );
  }

  const maximum = Math.max(
    ...points.map(
      (point) => point.revenue
    ),
    1
  );

  return (
    <div className="monthly-chart">
      <div className="chart-grid">
        <div />
        <div />
        <div />
        <div />
      </div>

      <div className="chart-bars">
        {points.map((point, index) => {
          const height =
            (point.revenue /
              maximum) *
            100;

          return (
            <div
              className="monthly-column"
              key={`${point.month}-${index}`}
            >
              <div className="monthly-value">
                {formatCurrency(
                  point.revenue
                )}
              </div>

              <div className="monthly-bar-area">
                <div
                  className="monthly-bar"
                  style={{
                    height: `${height}%`,
                  }}
                />
              </div>

              <div className="monthly-label">
                {point.month}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

/* ============================================================
   PAGE
============================================================ */

export default function FinancialsPage() {
  const [summary, setSummary] =
    useState<AnalyticsSummary | null>(
      null
    );

  const [variance, setVariance] =
    useState<VarianceResponse | null>(
      null
    );

  const [monthlyRevenue, setMonthlyRevenue] =
    useState<MonthlyRevenueResponse | null>(
      null
    );

  const [businessUnits, setBusinessUnits] =
    useState<BusinessUnitsResponse | null>(
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
    async function loadFinancials() {
      try {
        setLoading(true);
        setError(null);

        const [
          summaryData,
          varianceData,
          monthlyData,
          businessUnitData,
        ] = await Promise.all([
          getSummary(),
          getVariance(),
          getMonthlyRevenue(),
          getBusinessUnits(),
        ]);

        setSummary(summaryData);
        setVariance(varianceData);
        setMonthlyRevenue(monthlyData);
        setBusinessUnits(
          businessUnitData
        );
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Unable to load financial data."
        );
      } finally {
        setLoading(false);
      }
    }

    loadFinancials();
  }, []);

  /* ----------------------------------------------------------
     DERIVED METRICS
  ---------------------------------------------------------- */

  const metrics = useMemo(() => {
    if (!summary || !variance) {
      return null;
    }

    const revenue =
      summary.finance.actual_revenue;

    const budget =
      summary.budget.budget_revenue;

    const cost =
      summary.finance.actual_cost;

    const contractValue =
      summary.finance.contract_value;

    const revenueVariance =
      revenue - budget;

    const margin =
      revenue !== 0
        ? ((revenue - cost) /
            revenue) *
          100
        : 0;

    return {
      revenue,
      budget,
      cost,
      contractValue,
      revenueVariance,
      margin,
    };
  }, [summary, variance]);

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
                Loading financial data
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
              FINANCIALS
            </div>

            <h1>
              Unable to load financial data
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

  if (!summary || !variance || !metrics) {
    return null;
  }

  /* ----------------------------------------------------------
     RENDER
  ---------------------------------------------------------- */

  return (
    <main className="app-shell">
      <Sidebar />

      <section className="main-content">
        {/* ====================================================
            HEADER
        ==================================================== */}

        <header className="topbar">
          <div>
            <div className="eyebrow">
              DELIVERY FINANCE
            </div>

            <h1>
              Financials
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
                Revenue
              </div>

              <div className="metric-value">
                {formatCurrency(
                  metrics.revenue
                )}
              </div>

              <div
                className={
                  metrics.revenueVariance >=
                  0
                    ? "metric-change positive"
                    : "metric-change negative"
                }
              >
                {formatPercent(
                  variance.actual_vs_budget_pct
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
                Revenue plan
              </div>
            </div>

            <div className="metric-block">
              <div className="metric-label">
                Actual cost
              </div>

              <div className="metric-value">
                {formatCurrency(
                  metrics.cost
                )}
              </div>

              <div className="metric-secondary">
                Delivery cost
              </div>
            </div>

            <div className="metric-block">
              <div className="metric-label">
                Contract value
              </div>

              <div className="metric-value">
                {formatCurrency(
                  metrics.contractValue
                )}
              </div>

              <div className="metric-secondary">
                Current contract value
              </div>
            </div>
          </section>

          {/* ==================================================
              REVENUE VS BUDGET
          ================================================== */}

          <section className="section">
            <div className="section-header">
              <div>
                <div className="section-kicker">
                  PERFORMANCE
                </div>

                <h2>
                  Revenue vs budget
                </h2>
              </div>

              <div className="section-meta">
                Actual performance
              </div>
            </div>

            <div className="panel financial-comparison-panel">
              <RevenueComparison
                actual={
                  variance.actual
                }
                budget={
                  variance.budget
                }
              />
            </div>
          </section>

          {/* ==================================================
              VARIANCE DETAIL
          ================================================== */}

          <section className="section">
            <div className="section-header">
              <div>
                <div className="section-kicker">
                  VARIANCE
                </div>

                <h2>
                  Revenue variance
                </h2>
              </div>
            </div>

            <div className="variance-grid">
              <div className="panel variance-panel">
                <div className="panel-label">
                  Actual vs budget
                </div>

                <div
                  className={`analysis-value ${
                    variance.actual_vs_budget >=
                    0
                      ? "positive"
                      : "negative"
                  }`}
                >
                  {variance.actual_vs_budget >=
                  0
                    ? "+"
                    : "−"}

                  {formatCurrency(
                    Math.abs(
                      variance.actual_vs_budget
                    )
                  )}
                </div>

                <div className="analysis-note">
                  Current revenue variance
                </div>
              </div>

              <div className="panel variance-panel">
                <div className="panel-label">
                  Variance percentage
                </div>

                <div
                  className={`analysis-value ${
                    variance.actual_vs_budget_pct >=
                    0
                      ? "positive"
                      : "negative"
                  }`}
                >
                  {formatPercent(
                    variance.actual_vs_budget_pct
                  )}
                </div>

                <div className="analysis-note">
                  Actual relative to budget
                </div>
              </div>

              <div className="panel variance-panel">
                <div className="panel-label">
                  Forecast vs budget
                </div>

                <div
                  className={`analysis-value ${
                    variance.forecast_vs_budget >=
                    0
                      ? "positive"
                      : "negative"
                  }`}
                >
                  {variance.forecast_vs_budget >=
                  0
                    ? "+"
                    : "−"}

                  {formatCurrency(
                    Math.abs(
                      variance.forecast_vs_budget
                    )
                  )}
                </div>

                <div className="analysis-note">
                  Current forecast variance
                </div>
              </div>

              <div className="panel variance-panel">
                <div className="panel-label">
                  Forecast variance %
                </div>

                <div
                  className={`analysis-value ${
                    variance.forecast_vs_budget_pct >=
                    0
                      ? "positive"
                      : "negative"
                  }`}
                >
                  {formatPercent(
                    variance.forecast_vs_budget_pct
                  )}
                </div>

                <div className="analysis-note">
                  Forecast relative to budget
                </div>
              </div>
            </div>
          </section>

          {/* ==================================================
              MONTHLY REVENUE
          ================================================== */}

          <section className="section">
            <div className="section-header">
              <div>
                <div className="section-kicker">
                  PERFORMANCE
                </div>

                <h2>
                  Monthly revenue
                </h2>
              </div>

              <div className="section-meta">
                Actual revenue
              </div>
            </div>

            <div className="panel monthly-revenue-panel">
              {monthlyRevenue ? (
                <MonthlyRevenueChart
                  data={
                    monthlyRevenue
                  }
                />
              ) : (
                <div className="empty-chart">
                  Revenue history unavailable.
                </div>
              )}
            </div>
          </section>

          {/* ==================================================
              BUSINESS UNITS
          ================================================== */}

          <section className="section">
            <div className="section-header">
              <div>
                <div className="section-kicker">
                  BUSINESS UNITS
                </div>

                <h2>
                  Financial performance
                </h2>
              </div>

              <div className="section-meta">
                Revenue and margin
              </div>
            </div>

            <div className="panel table-panel">
              {!businessUnits ||
              !businessUnits.value?.length ? (
                <div className="empty-table">
                  Business unit data unavailable.
                </div>
              ) : (
                <div className="financial-table">
                  <div className="financial-table-row financial-table-header">
                    <span>
                      Business unit
                    </span>

                    <span>
                      Actual
                    </span>

                    <span>
                      Budget
                    </span>

                    <span>
                      Variance
                    </span>

                    <span>
                      Margin
                    </span>

                    <span>
                      Cost
                    </span>
                  </div>

                  {businessUnits.value.map(
                    (unit) => (
                      <div
                        className="financial-table-row"
                        key={
                          unit.business_unit
                        }
                      >
                        <span className="unit-name">
                          {
                            unit.business_unit
                          }
                        </span>

                        <strong>
                          {formatCurrency(
                            unit.actual_revenue
                          )}
                        </strong>

                        <span>
                          {formatCurrency(
                            unit.budget_revenue
                          )}
                        </span>

                        <span
                          className={
                            unit.variance >=
                            0
                              ? "table-positive"
                              : "table-negative"
                          }
                        >
                          {formatPercent(
                            unit.variance_pct
                          )}
                        </span>

                        <span>
                          {formatPlainPercent(
                            unit.gross_margin_pct
                          )}
                        </span>

                        <span>
                          {formatCurrency(
                            unit.actual_cost
                          )}
                        </span>
                      </div>
                    )
                  )}
                </div>
              )}
            </div>
          </section>

          {/* ==================================================
              FINANCIAL POSITION
          ================================================== */}

          <section className="section">
            <div className="section-header">
              <div>
                <div className="section-kicker">
                  FINANCIAL POSITION
                </div>

                <h2>
                  Revenue and cost position
                </h2>
              </div>
            </div>

            <div className="position-grid">
              <div className="panel position-panel">
                <div className="panel-label">
                  Revenue
                </div>

                <div className="panel-value">
                  {formatCurrency(
                    metrics.revenue
                  )}
                </div>

                <div className="panel-note">
                  Actual revenue
                </div>
              </div>

              <div className="panel position-panel">
                <div className="panel-label">
                  Cost
                </div>

                <div className="panel-value">
                  {formatCurrency(
                    metrics.cost
                  )}
                </div>

                <div className="panel-note">
                  Actual delivery cost
                </div>
              </div>

              <div className="panel position-panel">
                <div className="panel-label">
                  Gross contribution
                </div>

                <div className="panel-value">
                  {formatCurrency(
                    metrics.revenue -
                      metrics.cost
                  )}
                </div>

                <div className="panel-note">
                  Revenue less cost
                </div>
              </div>

              <div className="panel position-panel">
                <div className="panel-label">
                  Gross margin
                </div>

                <div className="panel-value">
                  {formatPlainPercent(
                    metrics.margin
                  )}
                </div>

                <div className="panel-note">
                  Revenue margin
                </div>
              </div>
            </div>
          </section>
        </div>
      </section>
    </main>
  );
}