# LogHub Backend

This repository contains a simple FastAPI server with a SQLite database.

## Build and Run with Docker

```bash
# Build the Docker image
docker build -f docker/Dockerfile -t loghub-backend .

# Run the container
docker run -p 8000:8000 loghub-backend
```

The server will be available at `http://localhost:8000/` and includes CRUD endpoints for QSO records:

- `POST /qsos` create a QSO
- `GET /qsos` list QSOs
- `GET /qsos/{id}` retrieve a QSO
- `PUT /qsos/{id}` update a QSO
- `DELETE /qsos/{id}` remove a QSO

All data is stored in a SQLite database file `qso.db` located in the working directory.

## Local Development
To run the application or tests locally without Docker, install the Python dependencies and then run the server or `pytest` directly:

```bash
python -m pip install -r requirements.txt
```
The application creates the required tables automatically on startup.
