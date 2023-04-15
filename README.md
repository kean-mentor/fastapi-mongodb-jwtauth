# fastapi-mongodb-jwtauth
Tutorial project to learn FastAPI and JWT authentication &amp; authorization 

### Starting MongoDB server
- Edit `docker-compose.yml` if you want
- Create a file named `.env` with the following content:
  - `MONGO_INITDB_ROOT_USERNAME=<username>`
  - `MONGO_INITDB_ROOT_PASSWORD=<password>`
  - `MONGO_INITDB_DATABASE<database-name>`
- Run `docker compose up -d` to start

### Starting the FastAPI app using uvicorn
- Run `uvicorn app.main:app --host localhost --port 8000 --reload`
