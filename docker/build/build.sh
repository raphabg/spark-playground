#!/bin/bash
set -e

IMAGE_NAME="balogo-spark-4.0.0:latest"

echo "=== Building Spark Docker Image ($IMAGE_NAME) ==="
docker build -t $IMAGE_NAME ../

echo "=== Starting Spark Cluster with docker-compose ==="
docker-compose up -d

echo "=== Spark Cluster Started ==="
echo "Master UI: http://localhost:8080"
echo "History Server UI: http://localhost:18080"
