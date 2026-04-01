import os
import tempfile
import pytest
from httpx import AsyncClient, ASGITransport
from phone_agent.main import app
from phone_agent.config import settings

HEADERS = {"Authorization": "Bearer test-key"}


@pytest.fixture(autouse=True)
def set_key(monkeypatch):
    monkeypatch.setattr(settings, "phone_agent_key", "test-key")


@pytest.mark.asyncio
async def test_read_file():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write("hello test content")
        path = f.name
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.get("/files", params={"path": path}, headers=HEADERS)
        assert resp.status_code == 200
        assert resp.json()["content"] == "hello test content"
    finally:
        os.unlink(path)


@pytest.mark.asyncio
async def test_read_missing_file():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/files", params={"path": "/nonexistent/file.txt"}, headers=HEADERS)
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_write_and_read_file():
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "test.txt")
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.post("/files", json={"path": path, "content": "written"}, headers=HEADERS)
            assert resp.status_code == 200
            resp = await client.get("/files", params={"path": path}, headers=HEADERS)
            assert resp.json()["content"] == "written"


@pytest.mark.asyncio
async def test_list_directory():
    with tempfile.TemporaryDirectory() as d:
        open(os.path.join(d, "a.txt"), "w").close()
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.get("/files/list", params={"path": d}, headers=HEADERS)
        assert resp.status_code == 200
        names = [e["name"] for e in resp.json()["entries"]]
        assert "a.txt" in names


@pytest.mark.asyncio
async def test_relative_path_rejected():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/files", params={"path": "relative/path.txt"}, headers=HEADERS)
    assert resp.status_code == 400
