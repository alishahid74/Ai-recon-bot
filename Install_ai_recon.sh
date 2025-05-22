#!/bin/bash

echo "[+] Setting up AI Recon Bot environment..."

# Detect shell configuration file
if [[ "$SHELL" == */zsh ]]; then
    SHELL_RC="$HOME/.zshrc"
elif [[ "$SHELL" == */bash ]]; then
    SHELL_RC="$HOME/.bashrc"
else
    echo "[!] Unknown shell. Defaulting to ~/.bashrc"
    SHELL_RC="$HOME/.bashrc"
fi

# Install required Go tools
echo "[+] Installing subfinder and gau (if missing)..."
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/lc/gau/v2/cmd/gau@latest

# Add Go bin to PATH
echo "[+] Adding Go bin to PATH in $SHELL_RC"
echo 'export PATH=$PATH:$(go env GOPATH)/bin' >> "$SHELL_RC"
source "$SHELL_RC"

# Create and activate Python virtual environment
echo "[+] Creating Python virtual environment..."
python3 -m venv ai_recon_env
source ai_recon_env/bin/activate

# Install Python dependencies
echo "[+] Installing Python packages..."
pip install -r requirements.txt

echo "[+] Setup complete!"
echo "To run your bot: source ai_recon_env/bin/activate && python AI_bot.py"
