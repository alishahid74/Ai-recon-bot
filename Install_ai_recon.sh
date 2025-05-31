#!/bin/bash

echo "[+] Installing dependencies..."
sudo apt update && sudo apt install -y golang python3 python3-pip python3-venv git

echo "[+] Setting up Python virtual environment..."
python3 -m venv ai_recon_env
source ai_recon_env/bin/activate

echo "[+] Installing required Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

echo "[+] Installing subfinder..."
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

echo "[+] Installing gau..."
go install github.com/lc/gau/v2/cmd/gau@latest

echo "[+] Adding Go binaries to PATH..."
echo 'export PATH=$PATH:$(go env GOPATH)/bin' >> ~/.bashrc
source ~/.bashrc

echo "[+] All set. You can now activate the environment and run the tool:"
echo "source ai_recon_env/bin/activate && python AI_Bot.py --domain example.com"

