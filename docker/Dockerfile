FROM python:3.11-slim
WORKDIR /app

# Install Python dependencies first so they can be cached separately from the
# application source code.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source after installing requirements to take advantage of
# Docker layer caching when dependencies do not change.
COPY ./backend ./backend

EXPOSE 8000
CMD ["python", "-m", "backend.main"]
