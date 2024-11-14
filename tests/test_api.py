from app import app
from helpers import query_helpers
import pytest
import database_system.core


@pytest.fixture
def client():
    # Gives test cases access a temporary instance of the API
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture()
def setup_property():
    # Create a test property to be used by endpoint tests that require a pre-existing property
    conn = database_system.core.get_connection()
    test_property = {
        "address": "123 Test Avenue",
        "postcode": "TEST123",
        "city": "Testville",
        "num_rooms": 3,
        "created_by": 1
    }
    current_property_id = query_helpers.write_new_property(conn, test_property)
    conn.close()
    # Pause here giving test access to a property ID known to exist
    yield current_property_id
    # Clean up after test is done
    conn = database_system.core.get_connection()
    query_helpers.delete_property_by_id(conn, current_property_id)
    conn.close()


def test_get_all_properties(client):
    test_endpoint = "/api/properties"
    response = client.get(test_endpoint)
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_get_single_property(client, setup_property):
    current_property_id = setup_property
    test_endpoint = f"/api/properties/{current_property_id}"
    response = client.get(test_endpoint)
    assert response.status_code == 200
    assert response.json["property_id"] == current_property_id
