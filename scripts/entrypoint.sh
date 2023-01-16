#!/bin/bash
#
# Performs operations for the production-ready application. Runs migrations and
# start the application server.

cd src/ || exit 1
alembic upgrade head
python main.py
