"use client";

import { useEffect, useMemo, useState } from "react";

import {
  getBusinessUnits,
  getForecast,
  getIntelligence,
  getMonthlyRevenue,
  getSummary,
} from "@/lib/api";

import type {
  AnalyticsSummary,
  MonthlyRevenueResponse,
} from "@/types/analytics";
import type { ForecastCurrentResponse } from "@/types/forecast";
import type { IntelligenceOverview } from "@/types/intelligence";
import type { BusinessUnitsResponse } from "@/types/business-units";

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
  const date = new Date(`${month}-01`);

  if (Number.isNaN(date.getTime())) {
    return month;
  }

  return date.toLocaleDateString("en-US", {
    month: "short",
  });
}

function RevenueChart({ data }: { data: MonthlyRevenueResponse | null }) {
  if (!data?.value?.length) {
    return <div className="chart-empty">Revenue history unavailable.</div>;
  }

  const values = data.value;
  const max = Math.max(...values.map((item) => item.revenue));

  return (
    <div className="revenue-chart">
      <div className="chart-y-axis">
        <span>{formatCurrency(max)}</span>
        <span>{formatCurrency(max * 0.5)}</span>
        <span>₹0</span>
      </div>

      <div className="chart-area">
        <div className="chart-grid">
          <span />
          <span />
          <span />
        </div>

        <div className="chart-bars">
          {values.map((item) => {
            const height = max > 0 ? (item.revenue / max) * 100 : 0;

            return (
              <div className="chart-column" key={item.month}>
                <div className="chart-value">{formatCurrency(item.revenue)}</div>
                <div className="chart-bar" style={{ height: `${height}%` }} />
                <div className="chart-label">{monthLabel(item.month)}</div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

export default function Home() {
  const [summary, setSummary] = useState<AnalyticsSummary | null>(null);
  const [forecast, setForecast] = useState<ForecastCurrentResponse | null>(null);
  const [intelligence, setIntelligence] = useState<IntelligenceOverview | null>(null);
  const [monthlyRevenue, setMonthlyRevenue] = useState<MonthlyRevenueResponse | null>(null);
  const [businessUnits, setBusinessUnits] = useState<BusinessUnitsResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadDashboard() {
      try {
        setLoading(true);

        const [summaryData, forecastData, intelligenceData, revenueData, businessUnitData] =
          await Promise.all([
            getSummary(),
            getForecast(),
            getIntelligence(),
            getMonthlyRevenue(),
            getBusinessUnits(),
          ]);

        setSummary(summaryData);
        setForecast(forecastData);
        setIntelligence(intelligenceData);
        setMonthlyRevenue(revenueData);
        setBusinessUnits(businessUnitData);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Unable to load X-Fin data.");
      } finally {
        setLoading(false);
      }
    }

    loadDashboard();
  }, []);

  const observations = useMemo(() => {
    if (!summary || !forecast) return [];

    const revenueVariance = summary.finance.actual_revenue - summary.budget.budget_revenue;
    const forecastVariance = forecast.forecast.forecast_revenue - summary.budget.budget_revenue;
    const pipelineDependency =
      forecast.forecast.weighted_pipeline / forecast.forecast.forecast_revenue;

    return [
      `Revenue is ${formatCurrency(Math.abs(revenueVariance))} ${revenueVariance >= 0 ? "above" : "below"} budget.`,
      `Current forecast is ${formatCurrency(Math.abs(forecastVariance))} ${forecastVariance >= 0 ? "above" : "below"} budget.`,
      `${(pipelineDependency * 100).toFixed(1)}% of forecast revenue is supported by weighted pipeline.`,
      intelligence?.staffing
        ? `Delivery hours are ${Math.abs(intelligence.staffing.hours_variance_pct).toFixed(1)}% ${intelligence.staffing.hours_variance_pct >= 0 ? "above" : "below"} budget.`
        : "Staffing analysis is available in Operations.",
    ];
  }, [summary, forecast, intelligence]);

  if (loading) {
    return (
      <main className="app-shell">
        <div className="loading-screen">
          <div className="loading-mark">X</div>
          <div>
            <div className="loading-title">X-Fin</div>
            <div className="loading-subtitle">Loading financial data</div>
          </div>
        </div>
      </main>
    );
  }

  if (error) {
    return (
      <main className="app-shell">
        <div className="error-screen">
          <div className="eyebrow">SYSTEM STATUS</div>
          <h1>Unable to load financial data</h1>
          <p>{error}</p>
          <button onClick={() => window.location.reload()} className="secondary-button">
            Retry
          </button>
        </div>
      </main>
    );
  }

  if (!summary || !forecast) return null;

  const actualRevenue = summary.finance.actual_revenue;
  const budgetRevenue = summary.budget.budget_revenue;
  const forecastRevenue = forecast.forecast.forecast_revenue;

  const actualVariancePct = ((actualRevenue - budgetRevenue) / budgetRevenue) * 100;
  const forecastVariancePct = ((forecastRevenue - budgetRevenue) / budgetRevenue) * 100;

  return (
    <main className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">X</div>
          <div>
            <div className="brand-name">X-Fin</div>
            <div className="brand-caption">Delivery Finance</div>
          </div>
        </div>

        <nav className="navigation">
          <div className="nav-group">
            <div className="nav-heading">Workspace</div>
            <a className="nav-item active" href="#">Overview</a>
            <a className="nav-item" href="#">Financials</a>
            <a className="nav-item" href="#">Forecast</a>
            <a className="nav-item" href="#">Pipeline</a>
            <a className="nav-item" href="#">Operations</a>
          </div>

          <div className="nav-group">
            <div className="nav-heading">Analysis</div>
            <a className="nav-item" href="#">Scenarios</a>
          </div>
        </nav>

        <div className="sidebar-footer">
          <div className="status-label">Data status</div>
          <div className="status-row">
            <span className="status-dot" />
            <span>Connected</span>
          </div>
          <div className="status-detail">Finance data current</div>
        </div>
      </aside>

      <section className="main-content">
        <header className="topbar">
          <div>
            <div className="eyebrow">DELIVERY FINANCE</div>
            <h1>Overview</h1>
          </div>

          <div className="topbar-right">
            <div className="period">Current period</div>
            <div className="period-value">FY2026</div>
          </div>
        </header>

        <div className="content">
          <section className="metric-grid">
            <div className="metric-block">
              <div className="metric-label">Revenue</div>
              <div className="metric-value">{formatCurrency(actualRevenue)}</div>
              <div className="metric-change positive">
                {formatPercent(actualVariancePct)} <span>vs budget</span>
              </div>
            </div>

            <div className="metric-block">
              <div className="metric-label">Budget</div>
              <div className="metric-value">{formatCurrency(budgetRevenue)}</div>
              <div className="metric-secondary">Revenue plan</div>
            </div>

            <div className="metric-block">
              <div className="metric-label">Forecast</div>
              <div className="metric-value">{formatCurrency(forecastRevenue)}</div>
              <div className={`metric-change ${forecastVariancePct >= 0 ? "positive" : "negative"}`}>
                {formatPercent(forecastVariancePct)} <span>vs budget</span>
              </div>
            </div>

            <div className="metric-block">
              <div className="metric-label">Forward coverage</div>
              <div className="metric-value">{formatCurrency(forecast.backlog.total_coverage)}</div>
              <div className="metric-secondary">Backlog + pipeline</div>
            </div>
          </section>

          <section className="section">
            <div className="section-header">
              <div>
                <div className="section-kicker">PERFORMANCE</div>
                <h2>Revenue performance</h2>
              </div>
              <div className="section-meta">Monthly actual revenue</div>
            </div>

            <div className="panel chart-panel">
              <RevenueChart data={monthlyRevenue} />
            </div>
          </section>

          <section className="section">
            <div className="section-header">
              <div>
                <div className="section-kicker">FORWARD POSITION</div>
                <h2>Revenue outlook</h2>
              </div>
            </div>

            <div className="position-grid">
              <div className="panel position-panel">
                <div className="panel-label">Committed backlog</div>
                <div className="panel-value">{formatCurrency(forecast.backlog.committed_backlog)}</div>
                <div className="panel-note">Contracted revenue</div>
              </div>

              <div className="panel position-panel">
                <div className="panel-label">Weighted pipeline</div>
                <div className="panel-value">{formatCurrency(forecast.pipeline.weighted_pipeline)}</div>
                <div className="panel-note">Probability-weighted opportunities</div>
              </div>

              <div className="panel position-panel">
                <div className="panel-label">Forecast</div>
                <div className="panel-value">{formatCurrency(forecastRevenue)}</div>
                <div className="panel-note">Current operating forecast</div>
              </div>

              <div className="panel position-panel">
                <div className="panel-label">Budget</div>
                <div className="panel-value">{formatCurrency(budgetRevenue)}</div>
                <div className="panel-note">Revenue target</div>
              </div>
            </div>
          </section>

          <section className="section">
            <div className="section-header">
              <div>
                <div className="section-kicker">BUSINESS UNITS</div>
                <h2>Performance by unit</h2>
              </div>
            </div>

            <div className="panel table-panel">
              <table>
                <thead>
                  <tr>
                    <th>Business unit</th>
                    <th>Revenue</th>
                    <th>Budget variance</th>
                    <th>Gross margin</th>
                    <th>Hours</th>
                  </tr>
                </thead>
                <tbody>
                  {businessUnits?.value?.map((unit) => (
                    <tr key={unit.business_unit}>
                      <td className="table-primary">{unit.business_unit}</td>
                      <td>{formatCurrency(unit.actual_revenue)}</td>
                      <td className={unit.variance_pct >= 0 ? "table-positive" : "table-negative"}>
                        {formatPercent(unit.variance_pct)}
                      </td>
                      <td>{unit.gross_margin_pct.toFixed(1)}%</td>
                      <td>{formatHours(unit.actual_hours)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>

          <section className="section">
            <div className="section-header">
              <div>
                <div className="section-kicker">ANALYSIS</div>
                <h2>Key observations</h2>
              </div>
            </div>

            <div className="observations">
              {observations.map((observation, index) => (
                <div className="observation" key={index}>
                  <span className="observation-index">{String(index + 1).padStart(2, "0")}</span>
                  <span>{observation}</span>
                </div>
              ))}
            </div>
          </section>
        </div>
      </section>
    </main>
  );
}
