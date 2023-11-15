import pytest
from httpx import AsyncClient
from src.main import initialize_application


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def async_client():
    async with AsyncClient(
        app=initialize_application(), base_url="http://test"
    ) as async_client:
        print("Client is ready")
        yield async_client
