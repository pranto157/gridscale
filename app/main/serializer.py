from marshmallow import validates, ValidationError, validate
from marshmallow.decorators import post_load
from flasgger import Schema, fields

from app.errors.exceptions import CityDoesNotExists
from app.models.city import CityModel
from app.main.utils import (
    generate_uuid,
    BeautyEnum,
    MAX_LATITUDE,
    MIN_LATITUDE,
    MAX_LONGITUDE,
    MIN_LONGITUDE,
)


class CityRequestParamsSchema(Schema):
    name = fields.String()
    geo_location_latitude = fields.Float()
    geo_location_longitude = fields.Float()
    beauty = fields.String(validate=validate.OneOf([val.value for val in BeautyEnum]))


class BeautyEnumField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return value.value


class CityResponseSchema(Schema):
    city_uuid = fields.String()
    name = fields.String()
    geo_location_latitude = fields.Float()
    geo_location_longitude = fields.Float()
    beauty = BeautyEnumField(attribute="beauty")
    population = fields.Integer()
    allied_cities = fields.List(fields.String())


class CityResponseSingleResponseSchema(CityResponseSchema):
    allied_power = fields.Integer()


class CityRequestPOSTSchema(Schema):
    name = fields.String(required=True)
    geo_location_latitude = fields.Float(
        required=True, validate=validate.Range(min=MIN_LATITUDE, max=MAX_LATITUDE)
    )
    geo_location_longitude = fields.Float(
        required=True, validate=validate.Range(min=MIN_LONGITUDE, max=MAX_LONGITUDE)
    )
    beauty = fields.String(
        required=True, validate=validate.OneOf([val.value for val in BeautyEnum])
    )
    population = fields.Integer(required=True)
    allied_cities = fields.List(fields.String(), required=False)

    @post_load
    def set_default_uuid(self, data, **kwargs):
        if "city_uuid" not in data:
            data["city_uuid"] = generate_uuid()
        return data

    @validates("allied_cities")
    def validate_allied_cities(self, value):
        allied_cities = value or []

        # Perform validation logic here
        for city_uuid in allied_cities:
            try:
                CityModel.get_city_by_uuid(city_uuid)
            except CityDoesNotExists:
                raise ValidationError(
                    f"Allied City with UUID '{city_uuid}' does not exist"
                )


class CityRequestPUTSchema(Schema):
    name = fields.String(required=False)
    geo_location_latitude = fields.Float(required=False)
    geo_location_longitude = fields.Float(required=False)
    beauty = fields.String(
        required=False, validate=validate.OneOf([val.value for val in BeautyEnum])
    )
    population = fields.Integer(required=False)
    allied_cities = fields.List(fields.String(), required=False)

    @validates("geo_location_latitude")
    def validate_latitude(self, value):
        if value is not None and not (MIN_LATITUDE <= value <= MAX_LATITUDE):
            raise ValidationError(
                f"Latitude must be between {MIN_LATITUDE} and {MAX_LATITUDE}"
            )

    @validates("geo_location_longitude")
    def validate_longitude(self, value):
        if value is not None and not (MIN_LONGITUDE <= value <= MAX_LONGITUDE):
            raise ValidationError(
                f"Longitude must be between {MIN_LONGITUDE} and {MAX_LONGITUDE}"
            )
