from datetime import date
from typing import Optional
from pydantic import BaseModel, Field

class DanelfinRequest(BaseModel):
    date: date | None = Field(default=None, description="Query date in YYYY-MM-DD format")
    ticker: Optional[str] = Field(default=None, max_length=10, description="Ticker unique identifier (e.g., PYPL, AMZN, AAPL)")
    market: Optional[str] = Field(default=None, description="Market type, defaults to 'USA', can be 'europe'")
    aiscore: Optional[int] = Field(default=None, ge=1, le=10, description="AI score (1-10)")
    fundamental: Optional[int] = Field(default=None, ge=1, le=10, description="Fundamental score (1-10)")
    technical: Optional[int] = Field(default=None, ge=1, le=10, description="Technical score (1-10)")
    sentiment: Optional[int] = Field(default=None, ge=1, le=10, description="Sentiment score (1-10)")
    low_risk: Optional[int] = Field(default=None, ge=1, le=10, description="Low-risk score (1-10)")
    buy_track_record: Optional[bool] = Field(default=None, description="Filter tickers with buy track record")
    sell_track_record: Optional[bool] = Field(default=None, description="Filter tickers with sell track record")
    sector: Optional[str] = Field(default=None, description="Sector slug (available at /sectors endpoint)")
    industry: Optional[str] = Field(default=None, description="Industry slug (available at /industries endpoint)")
    fields: Optional[List[str]] = Field(default=None, description="Comma-separated list of fields to be exported")


