# LogHub Backend

This repository contains a minimal FastAPI server.

## Build and Run with Docker

```bash
# Build the Docker image
docker build -f docker/Dockerfile -t loghub-backend .

# Run the container
docker run -p 8000:8000 loghub-backend
```

The server will be available at `http://localhost:8000/` and will respond with `{"message": "Hello World"}`.

