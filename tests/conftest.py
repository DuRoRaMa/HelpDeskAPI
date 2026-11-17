import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.api.tickets import tickets


@pytest.fixture()
def client():
    with TestClient(app) as client:
        yield client

@pytest.fixture(autouse=True)
def clear_tickets():
    tickets.clear()
    yield
    tickets.clear()

