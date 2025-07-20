#!/bin/bash
set -e

echo "=== Restarting Spark Cluster ==="

# Stop and remove containers/volumes
./stop.sh

# Build image and start cluster
./build.sh

echo "=== Spark Cluster Restarted Successfully ==="
echo "Master UI: http://localhost:8080"
echo "History Server UI: http://localhost:18080"
