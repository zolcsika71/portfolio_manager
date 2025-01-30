from typing import Dict, Optional
from pydantic import BaseModel
from datetime import date



class DanelfinRequest(BaseModel):
    date: Optional[date] = None
    ticker: Optional[str] = None
    aiscore: Optional[int] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    buy_track_record: Optional[bool] = None
    sell_track_record: Optional[bool] = None
    fields: Optional[str] = None