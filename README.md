# fastapi-mongodb-jwtauth

Tutorial project to learn FastAPI and cookie based JWT authentication &amp; authorization

### Starting MongoDB server

-   Edit `docker-compose.yml` if you want
-   Create a file named `.env` with the following content:
    -   `MONGO_INITDB_ROOT_USERNAME=<username>`
    -   `MONGO_INITDB_ROOT_PASSWORD=<password>`
    -   `MONGO_INITDB_DATABASE=<database-name>`
-   Run `docker compose up -d` to start

### Starting the FastAPI app using uvicorn

-   Add the following entries to the `.env` file:
    -   `DATABASE_URL=<mongo-db-connection-string>`
    -   `ACCESS_TOKEN_EXPIRES_IN=<token-expiration-in-minutes>`
    -   `REFRESH_TOKEN_EXPIRES_IN=<token-expiration-in-minutes>`
    -   `JWT_ALGORITHM=<jwt-algorithm>`
    -   `CLIENT_ORIGIN=<client-host-and-port>`
    -   `JWT_PRIVATE_KEY=<base64-encoded-rsa-private-key>`
    -   `JWT_PUBLIC_KEY=<base64-encoded-rsa-public-key>`
-   Run `uvicorn app.main:app --host localhost --port 8000 --reload` to start the server

### Sources
1. https://jwt.io/introduction
2. https://codevoweb.com/api-with-python-fastapi-and-mongodb-jwt-authentication/
3. https://indominusbyte.github.io/fastapi-jwt-auth/
4. https://docs.pydantic.dev/
5. https://fastapi.tiangolo.com/
6. https://pymongo.readthedocs.io/en/stable/index.html
