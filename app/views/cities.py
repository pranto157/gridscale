from flask import current_app
from flask_restful import request
from flasgger import SwaggerView, swag_from

from marshmallow import ValidationError

from app.errors.exceptions import CityCreationError, CityDoesNotExists
from app.main.db import db
from app.main.serializer import (
    CityRequestParamsSchema,
    CityRequestPOSTSchema,
    CityRequestPUTSchema,
    CityResponseSchema,
    CityResponseSingleResponseSchema,
)
from app.models.city import CityModel


class CityListView(SwaggerView):
    @swag_from("swagger/get_cities.yml", methods=["GET"])
    def get(self):
        try:
            # Parse and validate the request params using schema
            params = CityRequestParamsSchema().load(request.args)
        except ValidationError as err:
            return {"message": "Validation error", "errors": err.messages}, 400

        cities = CityModel.query.filter_by(**params).all()
        # Serialize the list of cities using the CityResponseSchema
        serialized_cities = CityResponseSchema(many=True).dump(cities)
        return serialized_cities, 200

    @swag_from("swagger/post_cities.yml", methods=["POST"])
    def post(self):
        try:
            # Deserialize input using CityRequestPOSTSchema
            data = CityRequestPOSTSchema().load(request.get_json())
        except ValidationError as e:
            return {"message": "Validation error", "errors": e.messages}, 400

        try:
            # Create City object and add to database using the model method
            new_city = CityModel.create(data)
            serialized_city = CityResponseSchema().dump(new_city)
            return serialized_city, 201

        except CityCreationError as e:
            current_app.logger.error("City has been failed to create.")
            return {"message": e.messages}, e.status


class CityView(SwaggerView):
    @swag_from("swagger/get_city.yml", methods=["GET"])
    def get(self, city_uuid):
        # Retrieve a specific city from the database by UUID
        city = CityModel.query.filter_by(city_uuid=city_uuid).first()

        try:
            city = CityModel.get_city_by_uuid(city_uuid)
        except CityDoesNotExists as e:
            return {"message": "Validation error", "errors": e.messages}, e.status

        allied_power = city.get_allied_power()
        # Serialize the city using the CityResponseSchema
        serialized_city = CityResponseSingleResponseSchema().dump(city)
        if allied_power:
            serialized_city["allied_power"] = allied_power
        return serialized_city, 200

    @swag_from("swagger/delete_city.yml", methods=["DELETE"])
    def delete(self, city_uuid):
        try:
            city_deleted = CityModel.delete(city_uuid)
            if not city_deleted:
                current_app.logger.info(
                    f"City not found in the database. [(UUID={city_uuid})]"
                )
                return {"message": "City not found"}, 404

            current_app.logger.info(
                f"City has been deleted with all aligned city. [(UUID={city_uuid})]"
            )
            return {"message": "City deleted successfully"}, 200
        except CityDoesNotExists as e:
            return {"message": "Validation error", "errors": e.messages}, e.status

    @swag_from("swagger/update_city.yml", methods=["PUT"])
    def put(self, city_uuid):
        try:
            with db.session.begin():
                city = CityModel.get_city_by_uuid(city_uuid)
        except CityDoesNotExists as e:
            current_app.logger.info(
                f"City not found in the database. [(UUID={city_uuid})]"
            )
            return {"message": "Validation error", "errors": e.messages}, e.status

        try:
            data = CityRequestPUTSchema().load(request.get_json())
            with db.session.begin():
                city.update_from_request_data(data)
                db.session.commit()

            serialized_city = CityResponseSchema().dump(city)
            current_app.logger.info(f"City updated successfully. [(UUID={city_uuid})]")
            return serialized_city, 200

        except (ValidationError, CityDoesNotExists) as e:
            return {"message": "Validation error", "errors": e.messages}, 400
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error updating city: {str(e)}")
            return {"message": "Error updating city"}, 500
