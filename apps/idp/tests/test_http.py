from collections.abc import Iterator
import logging

from fastapi.testclient import TestClient
import pytest

from app.main import app


@pytest.fixture
def client() -> Iterator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client


def test_home_returns_html(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert "Our identity server is running" in response.text
    assert 'href="/health/live"' in response.text


def test_liveness_returns_json(client: TestClient) -> None:
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_unknown_route_returns_404(client: TestClient) -> None:
    response = client.get("/missing")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_wrong_method_returns_405(client: TestClient) -> None:
    response = client.post("/")
    assert response.status_code == 405
    assert "GET" in response.headers["allow"]


def test_request_logger_does_not_expose_query_values(
    client: TestClient, caplog: pytest.LogCaptureFixture
) -> None:
    with caplog.at_level(logging.INFO, logger="uvicorn.error"):
        client.get("/health/live?code=secret-example")
    messages = [r.getMessage() for r in caplog.records if r.name == "uvicorn.error"]
    assert "GET /health/live -> 200" in messages
    assert all("secret-example" not in message for message in messages)
