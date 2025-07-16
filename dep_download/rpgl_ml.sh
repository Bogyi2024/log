#!/bin/bash
set -e

# Install required Python packages
pip install requests
pip install huggingface-hub

# Download rapidgator.py and run it
curl -o rpgl_ml.py https://raw.githubusercontent.com/Bogyi2024/log/main/dep_download/rpgl_ml.py
python rpgl_ml.py

# Download huggingface.py and run it
curl -o huggingface.py https://raw.githubusercontent.com/Bogyi2024/log/main/dep_download/huggingface.py
python huggingface.py
