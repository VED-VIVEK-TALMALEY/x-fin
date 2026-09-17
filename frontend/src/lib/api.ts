import type {
  AnalyticsSummary,
  MonthlyRevenueResponse,
  VarianceResponse,
} from "@/types/analytics";

import type {
  ForecastCurrentResponse,
} from "@/types/forecast";

import type {
  IntelligenceOverview,
} from "@/types/intelligence";

import type {
  BusinessUnitsResponse,
  BusinessUnitPerformance,
} from "@/types/business-units";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL;

if (!API_URL) {
  throw new Error(
    "NEXT_PUBLIC_API_URL is not configured"
  );
}

async function request<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const response = await fetch(
    `${API_URL}${endpoint}`,
    {
      ...options,
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        ...options?.headers,
      },
      cache: "no-store",
    }
  );

  if (!response.ok) {
    let detail = "";

    try {
      const body = await response.json();
      detail = JSON.stringify(body);
    } catch {
      detail = await response.text();
    }

    throw new Error(
      `X-Fin API ${response.status}: ${detail}`
    );
  }

  return response.json();
}

/* ============================================================
   BASIC ANALYTICS
============================================================ */

export function getHealth() {
  return request("/health");
}

export function getSummary(): Promise<AnalyticsSummary> {
  return request<AnalyticsSummary>(
    "/analytics/summary"
  );
}

export function getVariance(): Promise<VarianceResponse> {
  return request<VarianceResponse>(
    "/analytics/variance"
  );
}

export function getForecast(): Promise<ForecastCurrentResponse> {
  return request<ForecastCurrentResponse>(
    "/forecast/current"
  );
}

export function getIntelligence(): Promise<IntelligenceOverview> {
  return request<IntelligenceOverview>(
    "/intelligence/overview"
  );
}

/* ============================================================
   MONTHLY REVENUE
============================================================ */

type RawMonthlyRevenuePoint = {
  month?: string;
  Month?: string;
  date?: string;
  period?: string;

  revenue?: number;
  Revenue?: number;
  actual_revenue?: number;
  actualRevenue?: number;

  hours?: number;
  Hours?: number;
  actual_hours?: number;

  cost?: number;
  Cost?: number;
  actual_cost?: number;
};

type RawMonthlyRevenueResponse =
  | RawMonthlyRevenuePoint[]
  | {
      value?: RawMonthlyRevenuePoint[];
      data?: RawMonthlyRevenuePoint[];
      Count?: number;
    };

function normalizeMonth(
  month: string
): string {
  const normalized =
    month.length === 7
      ? `${month}-01`
      : month;

  const date = new Date(normalized);

  if (Number.isNaN(date.getTime())) {
    return month;
  }

  return date.toLocaleDateString(
    "en-US",
    {
      month: "short",
    }
  );
}

function normalizeMonthlyRevenue(
  data: RawMonthlyRevenueResponse
): MonthlyRevenueResponse {
  let rows: RawMonthlyRevenuePoint[] = [];

  if (Array.isArray(data)) {
    rows = data;
  } else if (Array.isArray(data.value)) {
    rows = data.value;
  } else if (Array.isArray(data.data)) {
    rows = data.data;
  }

  return {
    value: rows
      .map((row) => {
        const month =
          row.month ??
          row.Month ??
          row.date ??
          row.period;

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
          month: normalizeMonth(month),
          revenue,
          hours: Number.isFinite(hours)
            ? hours
            : 0,
          cost: Number.isFinite(cost)
            ? cost
            : 0,
        };
      })
      .filter(
        (
          row
        ): row is {
          month: string;
          revenue: number;
          hours: number;
          cost: number;
        } => row !== null
      ),
    Count: rows.length,
  };
}

export async function getMonthlyRevenue(): Promise<MonthlyRevenueResponse> {
  const data =
    await request<RawMonthlyRevenueResponse>(
      "/analytics/monthly-revenue"
    );

  return normalizeMonthlyRevenue(data);
}

/* ============================================================
   BUSINESS UNITS
============================================================ */

type RawBusinessUnitsResponse =
  | BusinessUnitPerformance[]
  | {
      value?: BusinessUnitPerformance[];
      data?: BusinessUnitPerformance[];
      Count?: number;
    };

function normalizeBusinessUnits(
  data: RawBusinessUnitsResponse
): BusinessUnitsResponse {
  let rows: BusinessUnitPerformance[] =
    [];

  if (Array.isArray(data)) {
    rows = data;
  } else if (Array.isArray(data.value)) {
    rows = data.value;
  } else if (Array.isArray(data.data)) {
    rows = data.data;
  }

  return {
    value: rows,
    Count: rows.length,
  };
}

export async function getBusinessUnits(): Promise<BusinessUnitsResponse> {
  const data =
    await request<RawBusinessUnitsResponse>(
      "/analytics/business-units"
    );

  return normalizeBusinessUnits(data);
}

/* ============================================================
   EXECUTIVE / SCENARIOS
============================================================ */

export function getExecutiveBriefing() {
  return request(
    "/executive/briefing"
  );
}

export interface ScenarioRequest {
  base_revenue: number;
  pipeline_revenue: number;
  utilization: number;
  pipeline_conversion_change: number;
  utilization_change: number;
  billing_rate_change: number;
  slippage_rate: number;
}

export interface ScenarioResult {
  base_revenue: number;
  adjusted_pipeline: number;
  adjusted_utilization: number;
  scenario_revenue: number;
  revenue_change: number;
  revenue_change_pct: number;
}

export function runScenario(
  payload: ScenarioRequest
): Promise<ScenarioResult> {
  return request<ScenarioResult>(
    "/scenarios/run",
    {
      method: "POST",
      body: JSON.stringify(payload),
    }
  );
}