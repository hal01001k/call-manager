FROM python:3.12-slim

WORKDIR /app

RUN mkdir -p /app/data && chmod 777 /app/data


RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*


COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY backend /app/backend

ENV PYTHONPATH=/app

# Expose port
EXPOSE 8000

# Run command
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
