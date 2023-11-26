## Test Project Setup & Execution

### Requirements

- Ensure the existence of the `.env` file for Environment Variables.
- Run `docker-compose up --build` and wait for the server to start.
- Two containers, `api` and `postgres`, should be up and running.
- The API container runs on port `1337`, while the Database operates on port `5432`.
- To run the tests follow this command - `docker exec -it api pytest`, this will run the test inside container.

### Swagger Access

- Access Swagger UI for this project at [http://127.0.0.1:1337/apidocs/](http://127.0.0.1:1337/apidocs/).
- Explore various endpoints and their respective parameters/request bodies.

### API Endpoints

- `GET http://127.0.0.1:1337/api/cities` retrieves all cities. Apply filters for specific results.
- `POST http://127.0.0.1:1337/api/cities` creates a new city.
- `GET http://127.0.0.1:1337/api/city/{city_uuid}` retrieves a single city along with its allied power.
- `PUT http://127.0.0.1:1337/api/city/{city_uuid}` updates a city.
- `DELETE http://127.0.0.1:1337/api/city/{city_uuid}` deletes a city.

### Validation Rules

- `geo_location_latitude` should range between `-90` and `90`.
- `geo_location_longitude` should range between `-180` and `180`.
- For `POST` or `PUT` requests, `allied_cities` must reference existing cities in the database; otherwise, it raises a validation error.
- `allied_power` is accessible via `GET http://127.0.0.1:1337/api/city/{city_uuid}` and calculates based on specific requirements ([logic details](https://github.com/pranto157/gridscale/blob/master/app/models/city.py#L88-L112)).
- Other validations are implemented using Marshmallow serializers for parsing request data and parameters.

### Future Improvements

- Implement pagination for the `GET citites` API.
- Conduct thorough query optimization and refactoring to ensure DRY (Don't Repeat Yourself) principles are followed.


Read More API Doc:
- [`GET /api/cities`](https://github.com/pranto157/gridscale/wiki/GET--api-cities)
- [`POST /api/cities`](https://github.com/pranto157/gridscale/wiki/POST--api-cities)
- [`GET /api/city/{city_uuid}`](https://github.com/pranto157/gridscale/wiki/GET--api-city-%7Bcity_uuid%7D)
- [`PUT /api/city/{city_uuid}`](https://github.com/pranto157/gridscale/wiki/PUT--api-city-%7Bcity_uuid%7D)
- [`DELETE /api/city/{city_uuid}`](https://github.com/pranto157/gridscale/wiki/DELETE--api-city-%7Bcity_uuid%7D)
