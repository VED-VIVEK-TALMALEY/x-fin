export type Severity = "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
export type RiskLevel = "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";

export interface IntelligenceReasoning {
  performance: string;
  forecast_status: string;
  actual_revenue: number;
  budget_revenue: number;
  forecast_revenue: number;
  committed_backlog: number;
  weighted_pipeline: number;
  budget_gap: number;
  budget_gap_pct: number;
  forecast_gap: number;
  forecast_gap_pct: number;
  forward_revenue: number;
  forward_coverage: number;
  forward_position: string;
  committed_forecast_coverage: number;
  committed_revenue_mix: number;
  pipeline_dependency: number;
  forecast_risk: string;
  pipeline_risk: string;
  forecast_headroom: number;
  forecast_headroom_pct: number;
  forecast_confidence_base: number;
}

export interface IntelligenceRisk {
  overall_risk: string;
  forecast_risk: string;
  pipeline_risk: string;
  risk_score: number;
  risk_score_status: string;
  committed_forecast_coverage: number;
  pipeline_dependency: number;
  forecast_headroom: number;
  forecast_headroom_pct: number;
  risk_adjustment: number;
  risk_adjustment_pct: number;
  headroom_status: string;
}

export interface MonteCarloDeterministicInputs {
  actual_revenue: number;
  budget_revenue: number;
  committed_backlog: number;
  weighted_pipeline: number;
  utilization_adjustment: number;
  risk_adjustment: number;
}

export interface MonteCarloDistribution {
  p10: number;
  p25: number;
  p50: number;
  p75: number;
  p90: number;
  mean: number;
  standard_deviation: number;
  range_p10_p90: number;
}

export interface MonteCarloBudgetAnalysis {
  probability_above_budget: number;
  probability_below_budget: number;
  p10_vs_budget: number;
  p50_vs_budget: number;
  p90_vs_budget: number;
}

export interface MonteCarloRisk {
  risk_level: string;
  downside_at_p10: number;
  forecast_range: number;
}

export interface MonteCarloResult {
  iterations: number;
  random_seed: number;
  deterministic_inputs: MonteCarloDeterministicInputs;
  distribution: MonteCarloDistribution;
  budget_analysis: MonteCarloBudgetAnalysis;
  risk: MonteCarloRisk;
}

export interface Staffing {
  actual_hours: number;
  budget_hours: number;
  hours_attainment_pct: number;
  hours_variance: number;
  hours_variance_pct: number;
  actual_utilization: number | null;
  budget_utilization: number;
  utilization_gap: number | null;
  bench_hours: number | null;
  bench_percentage: number | null;
  actual_cost: number;
  blended_cost_per_hour: number;
  estimated_bench_cost: number | null;
  actual_revenue: number;
  realized_revenue_per_hour: number;
  potential_revenue: number | null;
  bench_margin_exposure: number | null;
  capacity_status: string;
  bench_risk: string;
  utilization_data_quality: string;
  capacity_measurement_note: string;
}

export interface Insight {
  severity: Severity;
  category: string;
  metric: string;
  message: string;
  value: number | null;
}

export interface Recommendation {
  priority: Severity;
  category: string;
  action: string;
  rationale: string;
  financial_impact: number;
}

export interface DataQualityFlag {
  severity: Severity;
  area: string;
  message: string;
}

export interface DataQuality {
  status: string;
  flags: DataQualityFlag[];
}

export interface SourceMetrics {
  actual_revenue: number;
  actual_cost: number;
  budget_revenue: number;
  budget_utilization: number;
  pipeline_value: number;
  weighted_pipeline: number;
  committed_backlog: number;
  uncommitted_pipeline: number;
}

export interface Forecast {
  committed_backlog: number;
  weighted_pipeline: number;
  utilization_adjustment: number;
  risk_adjustment: number;
  forecast_revenue: number;
}

export interface ForecastDecomposition {
  committed_backlog: number;
  weighted_pipeline: number;
  utilization_adjustment: number;
  risk_adjustment: number;
  forecast_revenue: number;
}

export interface IntelligenceOverview {
  status: string;
  canonical_forecast_revenue: number;
  reasoning: IntelligenceReasoning;
  risk: IntelligenceRisk;
  monte_carlo: MonteCarloResult;
  staffing: Staffing;
  insights: Insight[];
  recommendations: Recommendation[];
  staffing_insights: Insight[];
  staffing_recommendations: Recommendation[];
  data_quality: DataQuality;
  source_metrics: SourceMetrics;
  forecast: Forecast;
  forecast_decomposition: ForecastDecomposition;
}
