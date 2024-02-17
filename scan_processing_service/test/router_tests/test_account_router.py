import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_get_all_accounts(async_client: AsyncClient):
    response = await async_client.get("/v1/account")
    assert response.status_code == 404
