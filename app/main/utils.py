import uuid
from enum import Enum


def generate_uuid():
    return str(uuid.uuid4())


class BeautyEnum(str, Enum):
    UGLY = "ugly"
    AVERAGE = "average"
    GORGEOUS = "gorgeous"


MAX_DISTANCE = 10000
MIN_DISTANCE = 1000

MAX_LATITUDE = 90
MIN_LATITUDE = -90

MAX_LONGITUDE = 180
MIN_LONGITUDE = -180
