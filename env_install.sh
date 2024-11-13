#!/bin/bash

# Install Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
bash ~/miniconda.sh -b -p $HOME/miniconda
export PATH="$HOME/miniconda/bin:$PATH"
source ~/.bashrc

# Create and activate the Conda environment
conda create -n prodia python=3.12 -y
conda activate prodia

# Install Python dependencies
pip install -r requirements.txt