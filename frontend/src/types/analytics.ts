export interface FinanceSummary {
  actual_revenue: number;
  actual_cost: number;
  contract_value: number;
  planned_hours: number;
}

export interface BudgetSummary {
  budget_revenue: number;
  budget_hours: number;
  budget_utilization: number;
}

export interface BacklogSummary {
  committed_backlog: number;
  uncommitted_pipeline: number;
  total_coverage: number;
}

export interface AnalyticsSummary {
  finance: FinanceSummary;
  budget: BudgetSummary;
  backlog: BacklogSummary;
}

export interface MonthlyRevenuePoint {
  month: string;
  revenue: number;
  hours: number;
  cost: number;
}

export interface MonthlyRevenueResponse {
  value: MonthlyRevenuePoint[];
  Count: number;
}

export interface BacklogWaterfall {
  opening_backlog: number;
  new_wins: number;
  revenue_recognized: number | null;
  closing_backlog: number;
  methodology: string;
}

export interface BacklogResponse {
  summary: BacklogSummary;
  waterfall: BacklogWaterfall;
}

export interface VarianceResponse {
  actual: number;
  budget: number;
  forecast: number;
  actual_vs_budget: number;
  actual_vs_budget_pct: number;
  forecast_vs_budget: number;
  forecast_vs_budget_pct: number;
}