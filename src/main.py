from fastapi import FastAPI, HTTPException
from .models import DanelfinRequest
from .api_client import DanelfinClient

app = FastAPI(title="Danelfin API Client")
client = DanelfinClient()

@app.post("/api/data")
async def get_danelfin_data(request: DanelfinRequest):
    try:
        return await client.get_data(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e