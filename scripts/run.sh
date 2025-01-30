#!/bin/bash

cd "$(dirname "$0")"/.. || exit

# Start FastAPI server
echo "Starting FastAPI server..."
poetry run uvicorn src.portfolio_manager.main:app --reload

# Wait for FastAPI to start
sleep 2

# Start Streamlit app
echo "Starting Streamlit app..."
poetry run streamlit run src/portfolio_manager/streamlit_app.py



