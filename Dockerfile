FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application
COPY src/ ./src/
COPY models/ ./models/
COPY data/processed/ ./data/processed/

# Expose port - Render will set PORT env variable
EXPOSE 8000

# Run the application - use PORT from environment
CMD uvicorn src.model_serving:app --host 0.0.0.0 --port ${PORT:-8000}
