#!/bin/sh

# This script is the entrypoint for the Docker container.
# It ensures that database migrations are applied before the main application starts.

# The 'set -e' command ensures that the script will exit immediately if any command fails.
set -e

# 1. Apply Database Migrations
echo "Applying database migrations..."
alembic upgrade head

# 2. Start the Application
# The 'exec "$@"' command is a crucial part. It replaces the shell process
# with the command passed to the script. In our Dockerfile, this will be the
# 'uvicorn' command. This ensures that Uvicorn becomes the main process (PID 1)
# in the container, which is important for proper signal handling (like stopping the container).
echo "Starting application..."
exec "$@"