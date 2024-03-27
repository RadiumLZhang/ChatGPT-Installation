#!/bin/bash

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip and install required packages
pip install --upgrade pip
pip install "pyqt5<5.16" "pyqtwebengine<5.16" "black>=22.3.0"
pip install Flask Flask-SQLAlchemy

# Any additional setup commands can go here
# Run the following command in your terminal:
# chmod +x setup_env.sh