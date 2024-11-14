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
    yield current_property_id, test_property["created_by"]
    # Clean up after test is done
    conn = database_system.core.get_connection()
    query_helpers.delete_property_by_id(conn, current_property_id)
    conn.close()


# Test getting a list of all properties
def test_get_all_properties(client):
    test_endpoint = "/api/properties"
    response = client.get(test_endpoint)
    assert response.status_code == 200
    assert isinstance(response.json, list)


# Test retrieving a single property known to exist
def test_get_single_property(client, setup_property):
    current_property_id, _ = setup_property
    test_endpoint = f"/api/properties/{current_property_id}"
    response = client.get(test_endpoint)
    assert response.status_code == 200
    assert response.json["property_id"] == current_property_id


# Test retrieving a property that does not exist
def test_get_single_property_not_found(client):
    expected_response_message = "Property could not be found!"
    current_property_id = 0
    test_endpoint = f"/api/properties/{current_property_id}"
    response = client.get(test_endpoint)
    assert response.status_code == 404
    assert response.json["message"] == expected_response_message


# Test creating a property using data that should be valid
def test_create_property_valid(client):
    expected_response_message = "Property created"
    test_endpoint = "/api/properties"
    test_property_entry = {
        "address": "456 New Street",
        "postcode": "NEW456",
        "city": "New City",
        "num_rooms": 4,
        "created_by": 1
    }
    response = client.post(test_endpoint, json=test_property_entry)
    assert response.status_code == 201
    assert response.json["message"] == expected_response_message
    assert isinstance(response.json["property_id"], int)
    # Clean up after itself
    conn = database_system.core.get_connection()
    query_helpers.delete_property_by_id(conn, response.json["property_id"])
    conn.close()


# Test creating a property with a missing created_by field
def test_create_property_invalid_missing_user(client):
    expected_response_message = "Created_by user ID is required and must be an integer."
    test_endpoint = "/api/properties"
    test_property_entry = {
        "address": "456 New Street",
        "postcode": "NEW456",
        "city": "New City",
        "num_rooms": 4
    }
    response = client.post(test_endpoint, json=test_property_entry)
    assert response.status_code == 400
    assert response.json["message"]["created_by"] == expected_response_message


# Test creating a property with a missing num_rooms field
def test_create_property_invalid_missing_rooms(client):
    expected_response_message = "Number of rooms must be a positive integer."
    test_endpoint = "/api/properties"
    test_property_entry = {
        "address": "456 New Street",
        "postcode": "NEW456",
        "city": "New City",
        "created_by": 1
    }
    response = client.post(test_endpoint, json=test_property_entry)
    assert response.status_code == 400
    assert response.json["message"]["num_rooms"] == expected_response_message


# Test creating a property with a missing city field
def test_create_property_invalid_missing_city(client):
    expected_response_message = "City cannot be blank!"
    test_endpoint = "/api/properties"
    test_property_entry = {
        "address": "456 New Street",
        "postcode": "NEW456",
        "num_rooms": 4,
        "created_by": 1
    }
    response = client.post(test_endpoint, json=test_property_entry)
    assert response.status_code == 400
    assert response.json["message"]["city"] == expected_response_message


# Test creating a property with a missing postcode field
def test_create_property_invalid_missing_postcode(client):
    expected_response_message = "Postcode cannot be blank!"
    test_endpoint = "/api/properties"
    test_property_entry = {
        "address": "456 New Street",
        "city": "New City",
        "num_rooms": 4,
        "created_by": 1
    }
    response = client.post(test_endpoint, json=test_property_entry)
    assert response.status_code == 400
    assert response.json["message"]["postcode"] == expected_response_message


# Test creating a property with a missing address field
def test_create_property_invalid_missing_address(client):
    expected_response_message = "Address cannot be blank!"
    test_endpoint = "/api/properties"
    test_property_entry = {
        "postcode": "NEW456",
        "city": "New City",
        "num_rooms": 4,
        "created_by": 1
    }
    response = client.post(test_endpoint, json=test_property_entry)
    assert response.status_code == 400
    assert response.json["message"]["address"] == expected_response_message


# Test creating a property with an invalid created_by field
def test_create_property_invalid_user(client):
    expected_response_message = "Created_by user ID is required and must be an integer."
    test_endpoint = "/api/properties"
    test_property_entry = {
        "address": "456 New Street",
        "postcode": "NEW456",
        "city": "New City",
        "num_rooms": 4,
        "created_by": "1TEST"
    }
    response = client.post(test_endpoint, json=test_property_entry)
    assert response.status_code == 400
    assert response.json["message"]["created_by"] == expected_response_message


# Test creating a property with an invalid num_rooms field
def test_create_property_invalid_rooms(client):
    expected_response_message = "Number of rooms must be a positive integer."
    test_endpoint = "/api/properties"
    test_property_entry = {
        "address": "456 New Street",
        "postcode": "NEW456",
        "city": "New City",
        "num_rooms": "4TEST",
        "created_by": 1
    }
    response = client.post(test_endpoint, json=test_property_entry)
    assert response.status_code == 400
    assert response.json["message"]["num_rooms"] == expected_response_message


# Test Deleting a Property
def test_delete_property_valid(client, setup_property):
    property_id, created_by = setup_property
    deletion_headers = {"user_id": created_by}
    test_endpoint = f"/api/properties/{property_id}"
    response = client.delete(test_endpoint, headers=deletion_headers)
    assert response.status_code == 200
    assert response.json['message'] == "Property deleted successfully"
