#!/bin/bash
set -e  # Exit on any error

# Step 1: Install required Python package
echo "Installing huggingface-hub..."
pip install --quiet huggingface-hub

# Step 2: Download config file
echo "Downloading config.yml..."
curl -sSL -o config.yml https://raw.githubusercontent.com/Bogyi2024/log/refs/heads/main/pikpak/config.yml

# Step 3: Download PikPak CLI binary
echo "Downloading pikpakcli binary..."
curl -sSL -o pikpakcli https://github.com/Bogyi2024/log/raw/refs/heads/main/pikpak/pikpakcli

chmod +x pikpakcli
echo "Running pikpakcli..."
./pikpakcli download -p download

# Step 4: Download and run huggingface.py
echo "Downloading huggingface.py..."
curl -sSL -o huggingface.py https://raw.githubusercontent.com/Bogyi2024/log/main/dep_download/huggingface.py

echo "Running huggingface.py..."
python huggingface.py
