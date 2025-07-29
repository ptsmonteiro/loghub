FROM python:3.11-slim
WORKDIR /app
COPY ./backend ./backend
RUN pip install fastapi uvicorn sqlalchemy
EXPOSE 8000
CMD ["python", "-m", "backend.main"]
