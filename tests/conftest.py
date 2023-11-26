import pytest

from app.config import TestConfig
from app import create_app, db
from app.models.city import CityModel


@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def populated_db(app):
    # Add test data to the database
    city1 = CityModel(
        city_uuid="123",
        name="Test City 1",
        geo_location_latitude=30.0,
        geo_location_longitude=120.0,
        beauty="ugly",
        population=1000,
        allied_cities=[],
    )
    city2 = CityModel(
        city_uuid="456",
        name="Test City 2",
        geo_location_latitude=40.0,
        geo_location_longitude=150.0,
        beauty="gorgeous",
        population=2000,
        allied_cities=["123"],
    )

    city3 = CityModel(
        city_uuid="789",
        name="Test City 3",
        geo_location_latitude=-10.0,
        geo_location_longitude=-120.0,
        beauty="gorgeous",
        population=2000,
        allied_cities=["456"],
    )

    db.session.add(city1)
    db.session.add(city2)
    db.session.add(city3)
    db.session.commit()
