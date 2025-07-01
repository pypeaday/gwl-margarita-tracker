#!/bin/bash
set -e

export VIRTUAL_ENV=/opt/venv

# Start the application
exec uvicorn app.main:app --host 0.0.0.0 --port 8000


