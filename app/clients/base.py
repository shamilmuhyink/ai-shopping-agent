import httpx
from typing import Any, Dict, Optional

class BaseHttpClient:
    def __init__(self, base_url: str, default_headers: Optional[Dict[str, str]] = None):
        self.base_url = base_url
        self.default_headers = default_headers or {}
        self.client = httpx.AsyncClient(base_url=base_url, headers=self.default_headers, timeout=10.0)

    async def close(self) -> None:
        await self.client.aclose()

    async def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> httpx.Response:
        return await self.client.get(path, params=params)

    async def post(self, path: str, json: Optional[Dict[str, Any]] = None) -> httpx.Response:
        return await self.client.post(path, json=json)
