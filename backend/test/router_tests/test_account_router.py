import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_get_all_accounts(async_client: AsyncClient):
    response = await async_client.get("/v1/account")
    assert response.status_code == 200


@pytest.mark.anyio
async def test_create_account(async_client):
    response = await async_client.post(
        "/v1/account",
        json={"username": "test", "email": "test@gmx.de", "password": "Test1234!"},
    )
    assert response.status_code == 201
