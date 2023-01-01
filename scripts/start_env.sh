#!/bin/bash
#
# Starts all containers that are in the docker-compose.dev.yml file. The
# script will use environment variables from a .env.dist file.
#
# You may run a down_env.sh script to stop all running containers and remove
# them. stop_env.sh stops them without removing.

if docker-compose --env-file=.env.dist -f docker-compose.dev.yml up "$@"; then
  echo -e "\033[1;32mSuccess\033[0m"
else
  echo -e "\033[1;31mFailure\033[0m" && exit 1
fi
