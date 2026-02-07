# Use the official Python 3.11 slim image
FROM python:3.11-slim

# Environment settings for non-interactive builds
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install base system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create application directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml ./

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel \
    && pip install .

# Copy the rest of the application code
COPY . .

# Expose the API port
EXPOSE 7860

# API startup command
CMD ["bash", "-c", "python scripts/startup.py && uvicorn api.main:app --host 0.0.0.0 --port 7860"]
