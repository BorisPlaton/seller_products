#!/bin/bash
#
# Stops all containers that are in the docker-compose.dev.yml file and
# removes them. The script will use environment variables from a .env.dist

if docker-compose --env-file=.env.dist -f docker-compose.dev.yml down "$@"; then
  echo -e "\033[1;32mSuccess\033[0m"
else
  echo -e "\033[1;31mFailure\033[0m"
fi
