#!/bin/bash
set -e

echo "=== Spark Cluster Status ==="

# Show container statuses
docker ps --filter "name=spark-" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo
echo "Master UI:    http://localhost:8080"
echo "History UI:   http://localhost:18080"
