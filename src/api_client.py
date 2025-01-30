import httpx
from typing import Dict, Optional
from .config import settings
from .models import DanelfinRequest


class DanelfinClient:
    def __init__(self):
        self.base_url = settings.base_url
        self.headers = {"x-api-key": settings.api_key}

    async def get_data(self, params: DanelfinRequest) -> Dict:
        async with httpx.AsyncClient() as client:
            query_params = {k: v for k, v in params.dict().items() if v is not None}
            if params.date:
                query_params['date'] = params.date.strftime('%Y-%m-%d')

            response = await client.get(
                f"{self.base_url}/ranking",
                headers=self.headers,
                params=query_params
            )
            response.raise_for_status()
            return response.json()