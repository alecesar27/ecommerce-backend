import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, AsyncMock

client = TestClient(app)

@pytest.mark.asyncio
@patch("app.main.call_service", new_callable=AsyncMock)
async def test_graphql_proxy_user(mock_call):
    mock_call.return_value = {"data": {"user": {"username": "test"}}}
    response = client.post("/graphql", json={"query": "query { user(id: 1) { username } }"})
    assert response.status_code == 200
    assert "test" in response.json()["data"]["user"]["username"]
    mock_call.assert_called_with("http://user-service:8000/graphql", {"query": "query { user(id: 1) { username } }"})

@pytest.mark.asyncio
@patch("app.main.call_service", new_callable=AsyncMock)
async def test_graphql_proxy_unknown(mock_call):
    response = client.post("/graphql", json={"query": "query { unknown }"})
    assert response.status_code == 200
    assert "error" in response.json()