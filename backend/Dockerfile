FROM python:3.12-slim

WORKDIR /app

# Install system dependencies (curl for healthcheck if needed)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


ENV PYTHONPATH=/app

# exposed port
EXPOSE 8000

# command
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
