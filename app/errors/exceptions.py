class CityCreationError(Exception):
    def __init__(self):
        self.messages = "City has been failed to create"
        self.status = 400
        super().__init__(self.messages)


class CityDoesNotExists(Exception):
    def __init__(self, city_uuid):
        self.messages = f"City with UUID '{city_uuid}' does not exist in the database"
        self.status = 404
        super().__init__(self.messages)
