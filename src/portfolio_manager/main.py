from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import DanelfinRequest
from .api_client import DanelfinClient
import logging
from httpx import HTTPStatusError, RequestError, TimeoutException

app = FastAPI(title="Danelfin API Client")
client = DanelfinClient()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust to specific domains for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/data")
async def get_danelfin_data(request: DanelfinRequest):
    try:
        response = await client.get_data(request)
        return response
    except HTTPStatusError as e:
        logger.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except TimeoutException:
        logger.error("API request timed out")
        raise HTTPException(status_code=504, detail="API request timed out")
    except RequestError:
        logger.error("Network error")
        raise HTTPException(status_code=502, detail="Bad Gateway")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
