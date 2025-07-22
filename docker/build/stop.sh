#!/bin/bash
set -e

echo "=== Stopping Spark Cluster ==="

# Stop all services and remove containers, networks, and volumes created by docker-compose
docker-compose down -v 

echo "=== Spark Cluster Stopped and All Volumes Removed ==="
