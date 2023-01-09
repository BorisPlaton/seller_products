#!/bin/bash
#
# Connects to the database that is running in container.

source .env.dist
docker-compose -f docker-compose.dev.yml exec database psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"
