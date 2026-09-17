import type {
  AnalyticsSummary,
  MonthlyRevenueResponse,
} from "@/types/analytics";
import type { ForecastCurrentResponse } from "@/types/forecast";
import type { IntelligenceOverview } from "@/types/intelligence";
import type { ForecastAccuracyResponse } from "@/types/accuracy";
import type { BusinessUnitsResponse } from "@/types/business-units";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

if (!API_URL) {
  throw new Error("NEXT_PUBLIC_API_URL is not configured");
}

async function request<T>(
  endpoint: string,
  options?: RequestInit,
): Promise<T> {
  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
      ...options?.headers,
    },
    cache: "no-store",
  });

  if (!response.ok) {
    let detail = "";

    try {
      const body = await response.json();
      detail = JSON.stringify(body);
    } catch {
      detail = await response.text();
    }

    throw new Error(`X-Fin API ${response.status}: ${detail}`);
  }

  return response.json() as Promise<T>;
}

export function getHealth() {
  return request<{ status: string }>("/health");
}

export function getSummary() {
  return request<AnalyticsSummary>("/analytics/summary");
}

export function getMonthlyRevenue() {
  return request<MonthlyRevenueResponse>("/analytics/monthly-revenue");
}

export function getBacklog() {
  return request("/analytics/backlog");
}

export function getVariance() {
  return request("/analytics/variance");
}

export function getForecast() {
  return request<ForecastCurrentResponse>("/forecast/current");
}

export function getForecastAccuracy() {
  return request<ForecastAccuracyResponse>("/analytics/forecast-accuracy");
}

export function getBusinessUnits() {
  return request<BusinessUnitsResponse>("/analytics/business-units");
}

export function getIntelligence() {
  return request<IntelligenceOverview>("/intelligence/overview");
}

export function getExecutiveBriefing() {
  return request("/executive/briefing");
}

export function runScenario(payload: Record<string, unknown>) {
  return request("/scenarios/run", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}
