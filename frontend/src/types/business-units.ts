export interface BusinessUnitPerformance {
  business_unit: string;
  actual_revenue: number;
  budget_revenue: number;
  variance: number;
  variance_pct: number;
  actual_cost: number;
  gross_margin: number;
  gross_margin_pct: number;
  actual_hours: number;
  budget_hours: number;
}

export interface BusinessUnitsResponse {
  value: BusinessUnitPerformance[];
  Count: number;
}