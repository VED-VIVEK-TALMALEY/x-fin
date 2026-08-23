from pydantic import BaseModel, validator, conint, condecimal
from datetime import date
from enum import Enum
from typing import Optional
import uuid

class StageEnum(str, Enum):
    PROSPECT = "Prospect"
    QUALIFIED = "Qualified"
    IN_DELIVERY = "In Delivery"
    CLOSED_WON = "Closed Won"
    CLOSED_LOST = "Closed Lost"

class ProjectCreate(BaseModel):
    project_name: str
    business_unit: str
    client_name: str
    stage: StageEnum
    start_date: date
    end_date: Optional[date] = None
    billable_hours: conint(gt=0)
    bill_rate_per_hour: condecimal(decimal_places=2, gt=0)
    utilization_percent: conint(ge=0, le=100)
    win_probability: condecimal(decimal_places=2, ge=0, le=1)

class ProjectResponse(ProjectCreate):
    project_id: uuid.UUID
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True