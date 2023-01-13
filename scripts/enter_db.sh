#!/bin/bash
#
# Connects to the database that is running in the container.

ENV_FILE='.env.dist'

source "$ENV_FILE"
docker-compose --env-file "$ENV_FILE" -f docker-compose.dev.yml exec database psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"
