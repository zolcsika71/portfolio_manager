import httpx
from tenacity import retry, stop_after_attempt, wait_fixed
from .config import settings
from .models import DanelfinRequest
import logging

logger = logging.getLogger(__name__)

class DanelfinClient:
    def __init__(self):
        if not settings.base_url or not settings.api_key:
            raise ValueError("API base URL or API key is missing in configuration")
        
        self.base_url = settings.base_url
        self.headers = {"x-api-key": settings.api_key}

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))  # Retry 3 times with 2s delay
    async def get_data(self, params: DanelfinRequest):
        async with httpx.AsyncClient() as client:
            try:
                query_params = dict(params.dict(exclude_none=True).items())
                if params.date:
                    query_params['date'] = params.date.strftime('%Y-%m-%d')

                response = await client.get(
                    f"{self.base_url}/ranking",
                    headers=self.headers,
                    params=query_params
                )
                response.raise_for_status()
                return response.json()

            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
# sourcery skip: raise-specific-error
                raise Exception(
                    f"API responded with error {e.response.status_code}: {e.response.text}"
                ) from e
            except httpx.TimeoutException as e:
                logger.error("Request timed out")
# sourcery skip: raise-specific-error
                raise Exception("API request timed out") from e
            except httpx.RequestError as e:
                logger.error(f"Network error: {str(e)}")
# sourcery skip: raise-specific-error
                raise Exception("Network error while connecting to API") from e
