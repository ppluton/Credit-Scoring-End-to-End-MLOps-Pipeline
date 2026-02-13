import json

import pytest
from fastapi.testclient import TestClient

from api.app import app


@pytest.fixture(scope="session")
def client():
    """Client de test FastAPI avec lifespan (charge le modèle)."""
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def sample_payload():
    """Payload de test avec un vrai client."""
    with open("tests/fixtures/sample_client.json") as f:
        return json.load(f)
