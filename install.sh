#!/bin/bash

set -e  # Exit on first error

IMAGE_NAME="rag-assistant"
CONTAINER_NAME="rag-assistant-container"
PORT=8000
INTERNAL_PORT=7860

echo "Building Docker image '$IMAGE_NAME'..."
docker build -t $IMAGE_NAME .

echo "Removing existing container (if any)..."
docker rm -f $CONTAINER_NAME 2>/dev/null || true

echo "Running container '$CONTAINER_NAME' on port $PORT..."
docker run -d \
  --name $CONTAINER_NAME \
  --env-file .env \
  -p $PORT:$INTERNAL_PORT \
  $IMAGE_NAME

echo "Container is running. Access your API at: http://localhost:$PORT"
