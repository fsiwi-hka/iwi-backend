#!/bin/bash
set -e

echo "Stoppe laufende Container..."
docker compose down || true

echo "Baue neues Docker-Image..."
docker build -t flask-backend:latest .

echo "Starte die Container..."
docker compose up -d

echo "Cleanup ungenutzter Images..."
docker image prune -f

echo "Done!"