from datetime import date, timedelta
from typing import Optional
from pydantic import BaseModel, Field

class DanelfinRequest(BaseModel):
    """
    A model representing a user request with GUI-compatible fields.
    """
    date: Optional[date] = Field(
        default_factory=date.today,
        description="Select the query date (Today or Yesterday)."
    )
    ticker: Optional[str] = Field(
        default=None, max_length=10,
        description="Enter the stock ticker (e.g., AAPL, TSLA)."
    )
    market: Optional[str] = Field(
        default=None,
        description="Select the market type (e.g., Stock, Forex, Crypto)."
    )
    aiscore: Optional[int] = Field(default=None, ge=1, le=10, description="AI score (1-10).")
    fundamental: Optional[int] = Field(default=None, ge=1, le=10, description="Fundamental score (1-10).")
    technical: Optional[int] = Field(default=None, ge=1, le=10, description="Technical score (1-10).")
    sentiment: Optional[int] = Field(default=None, ge=1, le=10, description="Sentiment score (1-10).")
    low_risk: Optional[int] = Field(default=None, ge=1, le=10, description="Low-risk score (1-10).")
    buy_track_record: Optional[bool] = Field(default=None, description="Include buy track record.")
    sell_track_record: Optional[bool] = Field(default=None, description="Include sell track record.")
    sector: Optional[str] = Field(default=None, description="Select the sector.")
    industry: Optional[str] = Field(default=None, description="Select the industry.")
    fields: Optional[str] = Field(default=None, exclude=True, description="Feature disabled.")




