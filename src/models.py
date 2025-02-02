from enum import Enum  # Move this to the top
from datetime import date, timedelta
from typing import Optional
from pydantic import BaseModel, Field

class MarketType(str, Enum):
    STOCK = "Stock"
    FOREX = "Forex"
    CRYPTO = "Crypto"

market: Optional[MarketType] = Field(
    default=None,
    description="Select the market type (e.g., Stock, Forex, Crypto)."
)

from enum import Enum
class DanelfinRequest(BaseModel):
    class DanelfinRequest(BaseModel):
        date: Optional[date]
        ticker: Optional[str]
        market: Optional[str]
        aiscore: Optional[int]
    fundamental: Optional[int] = Field(default=None, ge=1, le=10, description="Fundamental score (1-10).")
    technical: Optional[int] = Field(default=None, ge=1, le=10, description="Technical score (1-10).")
    sentiment: Optional[int] = Field(default=None, ge=1, le=10, description="Sentiment score (1-10).")
    low_risk: Optional[int] = Field(default=None, ge=1, le=10, description="Low-risk score (1-10).")
    buy_track_record: Optional[bool] = Field(default=None, description="Include buy track record.")
    sell_track_record: Optional[bool] = Field(default=None, description="Include sell track record.")
    sector: Optional[str] = Field(default=None, description="Select the sector.")
    industry: Optional[str] = Field(default=None, description="Select the industry.")
    fields: Optional[str] = Field(
        default=None,
        description="Feature disabled.",
        deprecated=True
    )




