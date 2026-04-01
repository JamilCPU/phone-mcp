import pytest
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient, ASGITransport
from phone_agent.main import app
from phone_agent.config import settings
from phone_agent.utils.shell import ShellResult

HEADERS = {"Authorization": "Bearer test-key"}


@pytest.fixture(autouse=True)
def set_key(monkeypatch):
    monkeypatch.setattr(settings, "phone_agent_key", "test-key")


@pytest.mark.asyncio
async def test_shell_success():
    with patch("phone_agent.routes.shell.run_command", new_callable=AsyncMock) as mock_run:
        mock_run.return_value = ShellResult(stdout="hello world\n", stderr="", exit_code=0)
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.post("/shell", json={"command": "echo hello"}, headers=HEADERS)
    assert resp.status_code == 200
    assert resp.json()["exit_code"] == 0
    assert "hello world" in resp.json()["stdout"]


@pytest.mark.asyncio
async def test_shell_blocked_command(monkeypatch):
    monkeypatch.setattr(settings, "blocked_commands", "rm -rf /")
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post("/shell", json={"command": "rm -rf /"}, headers=HEADERS)
    assert resp.status_code == 200
    assert resp.json()["blocked"] is True


@pytest.mark.asyncio
async def test_shell_empty_command():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post("/shell", json={"command": ""}, headers=HEADERS)
    assert resp.status_code == 422
