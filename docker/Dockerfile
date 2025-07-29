FROM python:3.11-slim
WORKDIR /app
COPY ./backend ./backend
RUN pip install fastapi uvicorn
EXPOSE 8000
CMD ["python", "backend/main.py"]
