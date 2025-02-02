# src/models.py
from datetime import date
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

class ScoreType(str, Enum):
    AISCORE = "aiscore"
    TECHNICAL = "technical"
    LOW_RISK = "low_risk"
    SENTIMENT = "sentiment"
    FUNDAMENTAL = "fundamental"

class SectorList(str, Enum):
    COMMUNICATION = "communication-services"
    CONSUMER_DISCRETIONARY = "consumer-discretionary"
    CONSUMER_STAPLES = "consumer-staples"
    ENERGY = "energy"
    FINANCIALS = "financials"
    HEALTH_CARE = "health-care"
    INDUSTRIALS = "industrials"
    TECHNOLOGY = "information-technology"
    MATERIALS = "materials"
    REAL_ESTATE = "real-estate"
    UTILITIES = "utilities"

class DanelfinRequest(BaseModel):
    date: Optional[date] = None
    ticker: Optional[str] = None
    score_type: Optional[ScoreType] = None
    score_value: Optional[int] = Field(None, ge=1, le=10)
    buy_track_record: Optional[bool] = None
    sell_track_record: Optional[bool] = None
    sector: Optional[SectorList] = None
    industry: Optional[str] = None
    fields: Optional[str] = None




