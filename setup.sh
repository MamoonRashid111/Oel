#!/bin/bash

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# For Windows (Git Bash/WSL)
source venv/Scripts/activate || source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

echo "Environment setup complete. Activate the venv with 'source venv/Scripts/activate' (Bash) or '.\venv\Scripts\Activate.ps1' (PowerShell)."
