# Use Python 3.10 slim image (more stable for ML)
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY src/ ./src/
COPY models/ ./models/
COPY data/processed/ ./data/processed/

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "src.model_serving:app", "--host", "0.0.0.0", "--port", "8000"]
