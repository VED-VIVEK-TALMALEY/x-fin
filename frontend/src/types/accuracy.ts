export interface ForecastAccuracyPoint {
  month: string;
  actual_revenue: number;
  budget_revenue: number;
  variance_pct: number;
}

export interface ForecastAccuracyResponse {
  value: ForecastAccuracyPoint[];
  Count: number;
}
