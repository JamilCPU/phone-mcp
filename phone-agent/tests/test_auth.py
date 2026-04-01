import pytest
from httpx import AsyncClient, ASGITransport
from phone_agent.main import app
from phone_agent.config import settings


@pytest.fixture(autouse=True)
def set_key(monkeypatch):
    monkeypatch.setattr(settings, "phone_agent_key", "test-secret-key")


@pytest.mark.asyncio
async def test_health_no_auth():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/health")
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_shell_requires_auth():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post("/shell", json={"command": "echo hi"})
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_shell_invalid_token():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post(
            "/shell", json={"command": "echo hi"},
            headers={"Authorization": "Bearer wrong-key"},
        )
    assert resp.status_code == 401
