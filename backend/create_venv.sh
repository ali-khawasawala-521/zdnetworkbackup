#!/bin/bash

#Create Python virtual environment and install requirements

VENV_DIR="venv"

echo "Creating virtual environment in ./${VENV_DIR} ..."

# Check if python3 is installed
if ! command -v python3 &> /dev/null
then
    echo "python3 could not be found. Please install Python 3 first."
    exit 1
fi

# Create virtual environment
python3 -m venv "$VENV_DIR"

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Upgrade pip
pip install --upgrade pip

# Install requirements if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt ..."
    pip install -r requirements.txt
else
    echo "No requirements.txt found, skipping dependencies installation."
fi

echo "Virtual environment setup complete."
