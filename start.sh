#!/bin/bash
# FastAPI backend startup script

# Activate virtual environment
source venv/bin/activate

# Initialize database tables
echo "Initializing database..."
python -c "
import asyncio
from app.database import init_db
asyncio.run(init_db())
print('Database initialized successfully!')
"

# Start FastAPI server on port 3000 with host 0.0.0.0
echo "Starting FastAPI server on port 3000..."
uvicorn app.main:app --host 0.0.0.0 --port 3000 --reload
