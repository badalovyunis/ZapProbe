#!/bin/bash
# ZapProbe macOS Installation Script
# macOS Setup Script

set -e

echo ""
echo "======================================================"
echo "ZapProbe - macOS Installation"
echo "======================================================"
echo ""

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "[!] Homebrew not found"
    echo "[*] Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Install Python if needed
if ! command -v python3 &> /dev/null; then
    echo "[*] Installing Python 3..."
    brew install python3
fi

# Check Python version
echo "[*] Checking Python..."
PYTHON_VER=$(python3 --version 2>&1 | awk '{print $2}')
echo "[+] Python $PYTHON_VER found"

# Check pip
echo "[*] Checking pip..."
pip3 --version

# Install dependencies
echo ""
echo "[*] Installing dependencies..."
pip3 install -r requirements.txt
echo "[+] Dependencies installed"

# Install package
echo ""
echo "[*] Installing ZapProbe..."
pip3 install -e .
echo "[+] ZapProbe installed"

# Test installation
echo ""
echo "[*] Testing installation..."
if command -v zapprobe &> /dev/null; then
    zapprobe --version
    echo "[+] zapprobe command works!"
else
    echo "[!] zapprobe command not found"
    echo "[*] Trying with Python module..."
    python3 -m cli_runner --version
fi

echo ""
echo "======================================================"
echo "Installation Complete!"
echo "======================================================"
echo ""
echo "Usage:"
echo "  zapprobe --gui                    # GUI mode"
echo "  zapprobe URL                      # Quick scan"
echo "  zapprobe --help                   # Show help"
echo ""
