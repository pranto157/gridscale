from app.models.city import CityModel


def test_get_all_cities(client, populated_db):
    response = client.get("/api/cities")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert response.json == [
        {
            "city_uuid": "123",
            "name": "Test City 1",
            "geo_location_latitude": 30.0,
            "geo_location_longitude": 120.0,
            "beauty": "ugly",
            "population": 1000,
            "allied_cities": [],
        },
        {
            "city_uuid": "456",
            "name": "Test City 2",
            "geo_location_latitude": 40.0,
            "geo_location_longitude": 150.0,
            "beauty": "gorgeous",
            "population": 2000,
            "allied_cities": ["123"],
        },
        {
            "city_uuid": "789",
            "name": "Test City 3",
            "geo_location_latitude": -10.0,
            "geo_location_longitude": -120.0,
            "beauty": "gorgeous",
            "population": 2000,
            "allied_cities": ["456"],
        },
    ]


def test_create_city(client):
    data = {
        "name": "New City",
        "geo_location_latitude": 40.71,
        "geo_location_longitude": -74.01,
        "beauty": "gorgeous",
        "population": 3500000,
        "allied_cities": [],
    }

    response = client.post("/api/cities", json=data)
    assert response.status_code == 201


def test_update_city_allied_cities(client, populated_db):
    city_uuid_to_update = "123"
    allied_city_uuid = "789"

    # Prepare the data for the PUT request
    data = {"allied_cities": [allied_city_uuid]}

    # Make the PUT request to update the city's allied_cities
    response = client.put(f"/api/city/{city_uuid_to_update}", json=data)

    # Assert the response status code
    assert response.status_code == 200

    # Check if the response contains the updated allied_cities
    updated_city = CityModel.query.filter_by(city_uuid=city_uuid_to_update).first()
    assert updated_city.allied_cities == [allied_city_uuid]


def test_delete_city(client, populated_db):
    city_uuid_to_delete = "123"

    # Make the DELETE request to delete the city
    response = client.delete(f"/api/city/{city_uuid_to_delete}")

    # Assert the response status code
    assert response.status_code == 200

    # Check if the city has been deleted from the database
    deleted_city = CityModel.query.filter_by(city_uuid=city_uuid_to_delete).first()
    assert deleted_city is None

    # check allied city for 456 uuid
    city_456 = CityModel.query.filter_by(city_uuid="456").first()
    city_456.allied_cities is None


def test_update_city_with_invalid_allied_cities(client, populated_db):
    city_uuid_to_update = "123"
    allied_city_uuid = "test-uuid"

    # Prepare the data for the PUT request
    data = {"allied_cities": [allied_city_uuid]}

    # Make the PUT request to update the city's allied_cities
    response = client.put(f"/api/city/{city_uuid_to_update}", json=data)
    # Assert the response status code
    assert response.status_code == 400
    assert response.json == {
        "message": "Validation error",
        "errors": "City with UUID 'test-uuid' does not exist in the database",
    }
