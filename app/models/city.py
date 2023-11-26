from geopy.distance import geodesic
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, String
from sqlalchemy.orm.exc import NoResultFound

from app.errors.exceptions import CityDoesNotExists
from app.main.db import db
from app.main.utils import BeautyEnum, MAX_DISTANCE, MIN_DISTANCE


class CityModel(db.Model):
    __tablename__ = "cities"

    id = db.Column(db.Integer, primary_key=True)
    city_uuid = db.Column(db.String(36), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    geo_location_latitude = db.Column(db.Float, nullable=False)
    geo_location_longitude = db.Column(db.Float, nullable=False)
    beauty = db.Column(db.Enum(BeautyEnum), nullable=False)
    population = db.Column(db.BigInteger, nullable=False)
    allied_cities = db.Column(db.JSON)

    # Indexes for city_uuid and name columns
    __table_args__ = (
        db.Index("idx_city_uuid", city_uuid),
        db.Index("idx_name", name),
    )

    @staticmethod
    def get_city_by_uuid(city_uuid):
        try:
            return CityModel.query.filter_by(city_uuid=city_uuid).one()
        except NoResultFound:
            raise CityDoesNotExists(city_uuid)

    @staticmethod
    def create(data):
        try:
            city = CityModel(
                city_uuid=data["city_uuid"],
                name=data["name"],
                geo_location_latitude=data["geo_location_latitude"],
                geo_location_longitude=data["geo_location_longitude"],
                beauty=data["beauty"],
                population=data["population"],
                allied_cities=data.get("allied_cities", []),
            )

            db.session.add(city)
            db.session.commit()
            return city

        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete(city_uuid):
        try:
            aligned_cities = []
            with db.session.begin():
                city = CityModel.get_city_by_uuid(city_uuid)

            with db.session.begin():
                aligned_cities = (
                    db.session.query(CityModel)
                    .filter(
                        func.cast(CityModel.allied_cities, String).like(
                            f"%{city_uuid}%"
                        )
                    )
                    .all()
                )
        except SQLAlchemyError as e:
            db.session.rollback()  # Rollback the transaction in case of an error
            raise e

        for aligned_city in aligned_cities:
            aligned_city.allied_cities = [
                c for c in aligned_city.allied_cities if c != str(city_uuid)
            ]
            db.session.add(aligned_city)

        db.session.delete(city)
        db.session.commit()
        return True

    def get_allied_power(self):
        allied_power = self.population  # Initialize with the city's population

        if (
            not self.allied_cities
        ):  # No allies, return the city's population as allied power
            return None

        for ally_uuid in self.allied_cities:
            ally = CityModel.get_city_by_uuid(ally_uuid)

            if ally:
                distance = geodesic(
                    (self.geo_location_latitude, self.geo_location_longitude),
                    (ally.geo_location_latitude, ally.geo_location_longitude),
                ).kilometers

                if distance > MAX_DISTANCE:
                    allied_power += ally.population // 4  # Quartered
                elif distance > MIN_DISTANCE:
                    allied_power += ally.population // 2  # Halved
                else:
                    allied_power += ally.population

        return allied_power

    def update_from_request_data(self, data):
        new_allied_cities = data.get("allied_cities", self.allied_cities)

        # Validate if each UUID exists in the database before updating
        for city_uuid in new_allied_cities:
            CityModel.get_city_by_uuid(city_uuid)

        # If all UUIDs exist, update the allied_cities attribute
        self.allied_cities = new_allied_cities
        # Update other attributes as needed
        self.name = data.get("name", self.name)
        self.geo_location_latitude = data.get(
            "geo_location_latitude", self.geo_location_latitude
        )
        self.geo_location_longitude = data.get(
            "geo_location_longitude", self.geo_location_longitude
        )
        self.beauty = data.get("beauty", self.beauty)
        self.population = data.get("population", self.population)
