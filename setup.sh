#!/bin/bash

# Update and install necessary packages
sudo apt-get update
sudo apt-get install -y wget nginx

# Install Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
bash ~/miniconda.sh -b -p $HOME/miniconda
export PATH="$HOME/miniconda/bin:$PATH"
source ~/.bashrc

# Create and activate the Conda environment
conda create -n prodia python=3.12 -y
source $HOME/miniconda/bin/activate prodia

# Install Python dependencies
pip install -r requirements.txt

# Set up the Flask application
cd /home/your_user/your_project
export FLASK_APP=run.py
flask db upgrade  # If you are using Flask-Migrate

# Configure Nginx
sudo cp /home/your_user/your_project/nginx_config /etc/nginx/sites-available/your_project
sudo ln -s /etc/nginx/sites-available/your_project /etc/nginx/sites-enabled
sudo systemctl restart nginx

# Set up systemd service
sudo cp /home/your_user/your_project/your_project.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable your_project
sudo systemctl start your_project