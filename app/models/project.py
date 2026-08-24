from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ProjectStage(str, Enum):
    PROSPECT = "Prospect"
    QUALIFIED = "Qualified"
    IN_DELIVERY = "In Delivery"
    CLOSED_WON = "Closed Won"
    CLOSED_LOST = "Closed Lost"


class ProjectStatus(str, Enum):
    ACTIVE = "Active"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class ProjectCreate(BaseModel):
    project_name: str
    client_name: str
    business_unit: str
    stage: ProjectStage
    status: ProjectStatus = ProjectStatus.ACTIVE
    start_date: date
    end_date: Optional[date] = None
    contract_value: Decimal = Field(gt=0)
    billing_rate: Decimal = Field(gt=0)
    planned_hours: Decimal = Field(gt=0)


class ForecastRequest(BaseModel):
    project_id: Optional[UUID] = None
    forecast_month: date


class ScenarioRequest(BaseModel):
    pipeline_conversion_change: float = 0.0
    utilization_change: float = 0.0
    billing_rate_change: float = 0.0
    slippage_rate: float = 0.0