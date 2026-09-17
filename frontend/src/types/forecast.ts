export interface ForecastMetrics {
  committed_backlog: number;
  weighted_pipeline: number;
  utilization_adjustment: number;
  risk_adjustment: number;
  forecast_revenue: number;
}

export interface ForecastPipeline {
  opportunities: number;
  pipeline_value: number;
  weighted_pipeline: number;
}

export interface ForecastBacklog {
  committed_backlog: number;
  uncommitted_pipeline: number;
  total_coverage: number;
}

export interface ForecastAssumptions {
  current_utilization: number;
  target_utilization: number;
  execution_risk_rate: number;
}

export interface ForecastCurrentResponse {
  forecast: ForecastMetrics;
  pipeline: ForecastPipeline;
  backlog: ForecastBacklog;
  assumptions: ForecastAssumptions;
}