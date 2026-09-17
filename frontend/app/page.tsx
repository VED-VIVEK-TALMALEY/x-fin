"use client";

import { useEffect, useMemo, useState } from "react";
import Sidebar from "@/components/Sidebar";
import {
  getSummary,
  getForecast,
  getIntelligence,
  getMonthlyRevenue,
  getBusinessUnits,
} from "@/lib/api";

import type {
  AnalyticsSummary,
  MonthlyRevenueResponse,
} from "@/types/analytics";

import type { ForecastCurrentResponse } from "@/types/forecast";

import type { IntelligenceOverview } from "@/types/intelligence";

import type { BusinessUnitsResponse } from "@/types/business-units";

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

function formatHours(value: number) {
  return new Intl.NumberFormat("en-IN", {
    maximumFractionDigits: 0,
  }).format(value);
}

function monthLabel(month: string) {
  const normalized = month.length === 7
    ? `${month}-01`
    : month;

  const date = new Date(normalized);

  if (Number.isNaN(date.getTime())) {
    return month;
  }

  return date.toLocaleDateString("en-US", {
    month: "short",
  });
}

/* ============================================================
   MONTHLY REVENUE NORMALIZER
============================================================ */

interface NormalizedRevenuePoint {
  month: string;
  revenue: number;
  hours: number;
  cost: number;
}

function normalizeMonthlyRevenue(
  data: unknown
): NormalizedRevenuePoint[] {
  if (!data) {
    return [];
  }

  /*
   Expected backend shape:

   {
     value: [
       {
         month: "...",
         revenue: 123,
         hours: 123,
         cost: 123
       }
     ],
     Count: 12
   }
  */

  if (
    typeof data === "object" &&
    data !== null &&
    "value" in data
  ) {
    const value = (
      data as {
        value?: unknown;
      }
    ).value;

    if (Array.isArray(value)) {
      return value
        .map((item) => normalizeRevenuePoint(item))
        .filter(
          (
            item
          ): item is NormalizedRevenuePoint =>
            item !== null
        );
    }
  }

  /*
   Some FastAPI implementations may return:

   {
     data: [...]
   }
  */

  if (
    typeof data === "object" &&
    data !== null &&
    "data" in data
  ) {
    const value = (
      data as {
        data?: unknown;
      }
    ).data;

    if (Array.isArray(value)) {
      return value
        .map((item) => normalizeRevenuePoint(item))
        .filter(
          (
            item
          ): item is NormalizedRevenuePoint =>
            item !== null
        );
    }
  }

  /*
   Or simply:

   [...]
  */

  if (Array.isArray(data)) {
    return data
      .map((item) => normalizeRevenuePoint(item))
      .filter(
        (
          item
        ): item is NormalizedRevenuePoint =>
          item !== null
      );
  }

  return [];
}

function normalizeRevenuePoint(
  item: unknown
): NormalizedRevenuePoint | null {
  if (
    typeof item !== "object" ||
    item === null
  ) {
    return null;
  }

  const row =
    item as Record<string, unknown>;

  const month =
    typeof row.month === "string"
      ? row.month
      : typeof row.Month === "string"
        ? row.Month
        : typeof row.date === "string"
          ? row.date
          : typeof row.period === "string"
            ? row.period
            : null;

  if (!month) {
    return null;
  }

  const revenue = Number(
    row.revenue ??
      row.Revenue ??
      row.actual_revenue ??
      row.actualRevenue ??
      0
  );

  const hours = Number(
    row.hours ??
      row.Hours ??
      row.actual_hours ??
      0
  );

  const cost = Number(
    row.cost ??
      row.Cost ??
      row.actual_cost ??
      0
  );

  if (!Number.isFinite(revenue)) {
    return null;
  }

  return {
    month,
    revenue,
    hours: Number.isFinite(hours)
      ? hours
      : 0,
    cost: Number.isFinite(cost)
      ? cost
      : 0,
  };
}

/* ============================================================
   REVENUE CHART
============================================================ */

function RevenueChart({
  data,
}: {
  data: unknown;
}) {
  const points =
    normalizeMonthlyRevenue(data);

  if (!points.length) {
    return (
      <div className="chart-empty">
        Revenue history unavailable.
      </div>
    );
  }

  const maxRevenue = Math.max(
    ...points.map((item) => item.revenue)
  );

  const safeMax =
    maxRevenue > 0
      ? maxRevenue
      : 1;

  return (
    <div className="revenue-chart">
      <div className="chart-y-axis">
        <span>
          {formatCurrency(safeMax)}
        </span>

        <span>
          {formatCurrency(
            safeMax * 0.75
          )}
        </span>

        <span>
          {formatCurrency(
            safeMax * 0.5
          )}
        </span>

        <span>
          {formatCurrency(
            safeMax * 0.25
          )}
        </span>

        <span>₹0</span>
      </div>

      <div className="chart-area">
        <div className="chart-grid">
          <span />
          <span />
          <span />
          <span />
          <span />
        </div>

        <div className="chart-bars">
          {points.map((item) => {
            const height =
              (item.revenue / safeMax) *
              100;

            return (
              <div
                className="chart-column"
                key={`${item.month}-${item.revenue}`}
              >
                <div className="chart-value">
                  {formatCurrency(
                    item.revenue
                  )}
                </div>

                <div
                  className="chart-bar"
                  style={{
                    height: `${Math.max(
                      height,
                      2
                    )}%`,
                  }}
                  title={`${item.month}: ${formatCurrency(
                    item.revenue
                  )}`}
                />

                <div className="chart-label">
                  {monthLabel(
                    item.month
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

/* ============================================================
   PAGE
============================================================ */

export default function Home() {
  const [summary, setSummary] =
    useState<AnalyticsSummary | null>(
      null
    );

  const [forecast, setForecast] =
    useState<ForecastCurrentResponse | null>(
      null
    );

  const [intelligence, setIntelligence] =
    useState<IntelligenceOverview | null>(
      null
    );

  const [monthlyRevenue, setMonthlyRevenue] =
    useState<unknown>(null);

  const [businessUnits, setBusinessUnits] =
    useState<BusinessUnitsResponse | null>(
      null
    );

  const [error, setError] =
    useState<string | null>(null);

  const [loading, setLoading] =
    useState(true);

  /* ----------------------------------------------------------
     LOAD DATA
  ---------------------------------------------------------- */

  useEffect(() => {
    async function loadDashboard() {
      try {
        setLoading(true);
        setError(null);

        const [
          summaryData,
          forecastData,
          intelligenceData,
          revenueData,
          businessUnitData,
        ] = await Promise.all([
          getSummary(),
          getForecast(),
          getIntelligence(),
          getMonthlyRevenue(),
          getBusinessUnits(),
        ]);

        setSummary(summaryData);

        setForecast(forecastData);

        setIntelligence(
          intelligenceData
        );

        setMonthlyRevenue(
          revenueData
        );

        setBusinessUnits(
          businessUnitData
        );
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Unable to load X-Fin data."
        );
      } finally {
        setLoading(false);
      }
    }

    loadDashboard();
  }, []);

  /* ----------------------------------------------------------
     OBSERVATIONS
  ---------------------------------------------------------- */

  const observations = useMemo(() => {
    if (
      !summary ||
      !forecast
    ) {
      return [];
    }

    const revenueVariance =
      summary.finance.actual_revenue -
      summary.budget.budget_revenue;

    const forecastVariance =
      forecast.forecast.forecast_revenue -
      summary.budget.budget_revenue;

    const pipelineDependency =
      forecast.forecast
        .weighted_pipeline /
      forecast.forecast
        .forecast_revenue;

    const items = [
      `Revenue is ${formatCurrency(
        Math.abs(revenueVariance)
      )} ${
        revenueVariance >= 0
          ? "above"
          : "below"
      } budget.`,

      `Current forecast is ${formatCurrency(
        Math.abs(forecastVariance)
      )} ${
        forecastVariance >= 0
          ? "above"
          : "below"
      } budget.`,

      `${(
        pipelineDependency * 100
      ).toFixed(
        1
      )}% of forecast revenue is supported by weighted pipeline.`,
    ];

    if (intelligence?.staffing) {
      items.push(
        `Delivery hours are ${Math.abs(
          intelligence.staffing
            .hours_variance_pct
        ).toFixed(
          1
        )}% ${
          intelligence.staffing
            .hours_variance_pct >= 0
            ? "above"
            : "below"
        } budget.`
      );
    }

    return items;
  }, [
    summary,
    forecast,
    intelligence,
  ]);

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
              Loading financial data
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
            SYSTEM STATUS
          </div>

          <h1>
            Unable to load financial data
          </h1>

          <p>{error}</p>

          <button
            onClick={() =>
              window.location.reload()
            }
            className="secondary-button"
          >
            Retry
          </button>
        </div>
      </main>
    );
  }

  if (
    !summary ||
    !forecast
  ) {
    return null;
  }

  /* ----------------------------------------------------------
     CALCULATIONS
  ---------------------------------------------------------- */

  const actualRevenue =
    summary.finance.actual_revenue;

  const budgetRevenue =
    summary.budget.budget_revenue;

  const forecastRevenue =
    forecast.forecast
      .forecast_revenue;

  const actualVariancePct =
    ((actualRevenue -
      budgetRevenue) /
      budgetRevenue) *
    100;

  const forecastVariancePct =
    ((forecastRevenue -
      budgetRevenue) /
      budgetRevenue) *
    100;

  /* ----------------------------------------------------------
     RENDER
  ---------------------------------------------------------- */

  return (
    <main className="app-shell">
      {/* ======================================================
          SIDEBAR
      ====================================================== */}

     <Sidebar />
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
              Overview
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
              METRICS
          ================================================== */}

          <section className="metric-grid">
            <div className="metric-block">
              <div className="metric-label">
                Revenue
              </div>

              <div className="metric-value">
                {formatCurrency(
                  actualRevenue
                )}
              </div>

              <div className="metric-change positive">
                {formatPercent(
                  actualVariancePct
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
                  budgetRevenue
                )}
              </div>

              <div className="metric-secondary">
                Revenue plan
              </div>
            </div>

            <div className="metric-block">
              <div className="metric-label">
                Forecast
              </div>

              <div className="metric-value">
                {formatCurrency(
                  forecastRevenue
                )}
              </div>

              <div
                className={`metric-change ${
                  forecastVariancePct >=
                  0
                    ? "positive"
                    : "negative"
                }`}
              >
                {formatPercent(
                  forecastVariancePct
                )}

                <span>
                  vs budget
                </span>
              </div>
            </div>

            <div className="metric-block">
              <div className="metric-label">
                Forward coverage
              </div>

              <div className="metric-value">
                {formatCurrency(
                  forecast.backlog
                    .total_coverage
                )}
              </div>

              <div className="metric-secondary">
                Backlog + pipeline
              </div>
            </div>
          </section>

          {/* ==================================================
              REVENUE PERFORMANCE
          ================================================== */}

          <section className="section">
            <div className="section-header">
              <div>
                <div className="section-kicker">
                  PERFORMANCE
                </div>

                <h2>
                  Revenue performance
                </h2>
              </div>

              <div className="section-meta">
                Monthly actual revenue
              </div>
            </div>

            <div className="panel chart-panel">
              <RevenueChart
                data={monthlyRevenue}
              />
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
                  Revenue outlook
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
                  Probability-weighted opportunities
                </div>
              </div>

              <div className="panel position-panel">
                <div className="panel-label">
                  Forecast
                </div>

                <div className="panel-value">
                  {formatCurrency(
                    forecastRevenue
                  )}
                </div>

                <div className="panel-note">
                  Current operating forecast
                </div>
              </div>

              <div className="panel position-panel">
                <div className="panel-label">
                  Budget
                </div>

                <div className="panel-value">
                  {formatCurrency(
                    budgetRevenue
                  )}
                </div>

                <div className="panel-note">
                  Revenue target
                </div>
              </div>
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
                  Performance by unit
                </h2>
              </div>
            </div>

            <div className="panel table-panel">
              <table>
                <thead>
                  <tr>
                    <th>
                      Business unit
                    </th>

                    <th>
                      Revenue
                    </th>

                    <th>
                      Budget variance
                    </th>

                    <th>
                      Gross margin
                    </th>

                    <th>
                      Hours
                    </th>
                  </tr>
                </thead>

                <tbody>
                  {businessUnits?.value?.map(
                    (unit) => (
                      <tr
                        key={
                          unit.business_unit
                        }
                      >
                        <td className="table-primary">
                          {
                            unit.business_unit
                          }
                        </td>

                        <td>
                          {formatCurrency(
                            unit.actual_revenue
                          )}
                        </td>

                        <td
                          className={
                            unit.variance_pct >=
                            0
                              ? "table-positive"
                              : "table-negative"
                          }
                        >
                          {formatPercent(
                            unit.variance_pct
                          )}
                        </td>

                        <td>
                          {unit.gross_margin_pct.toFixed(
                            1
                          )}
                          %
                        </td>

                        <td>
                          {formatHours(
                            unit.actual_hours
                          )}
                        </td>
                      </tr>
                    )
                  )}
                </tbody>
              </table>
            </div>
          </section>

          {/* ==================================================
              ANALYSIS
          ================================================== */}

          <section className="section">
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
              {observations.map(
                (
                  observation,
                  index
                ) => (
                  <div
                    className="observation"
                    key={index}
                  >
                    <span className="observation-index">
                      {String(
                        index + 1
                      ).padStart(
                        2,
                        "0"
                      )}
                    </span>

                    <span>
                      {observation}
                    </span>
                  </div>
                )
              )}
            </div>
          </section>
        </div>
      </section>
    </main>
  );
}