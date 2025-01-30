from typing import Optional
from pydantic import BaseModel, Field
from datetime import date

class DanelfinRequest(BaseModel):
    date: Optional[date] = Field(None, description="Query date")
    ticker: Optional[str] = Field(None, max_length=10, description="Stock ticker symbol")
    aiscore: Optional[int] = Field(None, ge=1, le=10, description="AI score from 1 to 10")
    sector: Optional[str] = None
    industry: Optional[str] = None
    buy_track_record: Optional[bool] = None
    sell_track_record: Optional[bool] = None
    fields: Optional[str] = None
