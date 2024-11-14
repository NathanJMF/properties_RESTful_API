from app import app
import pytest


@pytest.fixture
def client():
    # Gives test cases access a temporary instance of the API
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_list_all_properties(client):
    test_endpoint = "/api/properties"
    response = client.get(test_endpoint)
    assert response.status_code == 200
    assert isinstance(response.json, list)
