import pytest
from fastapi.testclient import TestClient

from src.uno.app import create_app


@pytest.fixture
def client() -> TestClient:
    (app, _, _) = create_app()
    return TestClient(app)
