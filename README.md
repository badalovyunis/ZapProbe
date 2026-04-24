# ZapProbe Security Scanner

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-in%20development-yellow.svg)

An educational web vulnerability scanner for detecting SQL Injection and Cross-Site Scripting (XSS) vulnerabilities.

## 🚀 Quick Start

### Installation

#### **Linux (Recommended)**

```bash
# 1. Clone or download the repository
cd ZapProbe

# 2. Run automated setup (Linux only)
python3 linux_setup.py

# OR with GUI support:
python3 linux_setup.py --gui
```

**What it does:**

- ✅ Checks Python 3.8+
- ✅ Installs dependencies
- ✅ Installs ZapProbe globally
- ✅ Tests installation

#### **macOS**

```bash
# 1. Make script executable
chmod +x install_macos.sh

# 2. Run installation
./install_macos.sh
```

#### **Windows**

```batch
REM Double-click to run: install_windows.bat
REM Or from PowerShell:
.\install_windows.bat
```

#### **Manual Installation (All Platforms)**

```bash
# Basic installation
pip install -r requirements.txt

# With GUI support
pip install -r requirements.txt
pip install PySimpleGUI

# Install package (from ZapProbe directory)
pip install -e .

# Or with GUI:
pip install -e ".[gui]"
```

### Usage - 3 Easy Ways

#### 1️⃣ **GUI Mode (Easiest)**

```bash
zapprobe --gui
```

👉 Graphical interface opens with all options

#### 2️⃣ **Quick Scan (Fastest)**

```bash
zapprobe http://localhost:5000/search?id=1
```

👉 One command, full scan starts immediately

#### 3️⃣ **Advanced CLI (Most Control)**

```bash
# SQL Injection only
zapprobe http://localhost:5000/search?id=1 -t sqli

# XSS only with custom delay
zapprobe http://localhost:5000/comment?text=test -t xss --delay 2

# Generate HTML report
zapprobe http://localhost:5000/search?id=1 -o report.html

# Use with Burp Suite proxy
zapprobe http://localhost:5000/search?id=1 --proxy http://127.0.0.1:8080

# Disable SSL verification
zapprobe https://localhost:5443/search?id=1 --no-ssl-verify
```

### Advanced Examples

```bash
# Full scan with all options
zapprobe http://target.com/search?id=1 \
  -t all \
  --timeout 30 \
  --delay 1 \
  --proxy http://127.0.0.1:8080 \
  -o report.json

# Get help
zapprobe --help

# Check version
zapprobe --version
```

---

## 🐧 Linux-Specific Guide (For Linux Users)

### System Requirements

```bash
# Check requirements
python3 --version    # Should be 3.8+
pip3 --version       # Should be 23+
```

### Installation on Linux

#### **Option 1: Automated Setup (Recommended)**

```bash
# Download the project
git clone https://github.com/username/zapprobe.git
cd zapprobe

# Run automated setup
python3 linux_setup.py

# Or with GUI:
python3 linux_setup.py --gui
```

**This script:**

- Checks Python version
- Verifies pip installation
- Installs all dependencies
- Installs ZapProbe globally
- Tests the installation

#### **Option 2: Manual Installation**

```bash
# Update package manager
sudo apt-get update           # Ubuntu/Debian
sudo dnf update               # Fedora
sudo pacman -Sy               # Arch

# Install Python and pip
sudo apt-get install python3 python3-pip    # Ubuntu
sudo dnf install python3 python3-pip         # Fedora
sudo pacman -S python pip                    # Arch

# Clone and setup
git clone https://github.com/username/zapprobe.git
cd zapprobe

# Install Python dependencies
pip3 install -r requirements.txt

# Install package
pip3 install -e .

# Test installation
zapprobe --version
```

### Testing on Linux

#### **1. Start the Vulnerable Test Server**

```bash
# Terminal 1
cd examples/
python3 test_server.py
```

**Output:**

```
======================================================================
🚨 VULNERABLE TEST SERVER - EDUCATIONAL USE ONLY
======================================================================

📍 Server starting on http://localhost:5000
```

#### **2. Run Scanner in Another Terminal**

```bash
# Terminal 2
# Quick scan
zapprobe http://localhost:5000/search?id=1

# SQL Injection scan
zapprobe http://localhost:5000/search?id=1 -t sqli

# XSS scan
zapprobe http://localhost:5000/comment?text=test -t xss

# Full scan with report
zapprobe http://localhost:5000/search?id=1 -o report.html
```

#### **3. GUI Mode**

```bash
# First install PySimpleGUI if not already done
pip3 install PySimpleGUI

# Run GUI
zapprobe --gui
```

### Troubleshooting on Linux

#### **Problem: Command not found: zapprobe**

```bash
# Solution 1: Check where pip installed it
which zapprobe

# Solution 2: Use Python module directly
python3 -m cli_runner --help
python3 -m cli_runner http://localhost:5000/search?id=1

# Solution 3: Add to PATH manually
export PATH="$PATH:$HOME/.local/bin"
echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.bashrc
source ~/.bashrc

# Solution 4: Install with --user (if using system pip)
pip3 install --user -e .
```

#### **Problem: ImportError: No module named 'requests'**

```bash
# Solution: Install dependencies
pip3 install requests beautifulsoup4 colorama urllib3
# or
pip3 install -r requirements.txt
```

#### **Problem: Permission Denied on test_server.py**

```bash
# Make it executable
chmod +x examples/test_server.py

# Or run with python
python3 examples/test_server.py
```

#### **Problem: Port 5000 already in use**

```bash
# Find what's using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>

# Or use a different port (modify test_server.py):
# app.run(host='127.0.0.1', port=5001)
```

#### **Problem: SSL Certificate Error**

```bash
# Use --no-ssl-verify flag
zapprobe https://localhost:5443/search?id=1 --no-ssl-verify

# Or disable SSL in test server
# Change: app.run(ssl_context='adhoc')
# To: app.run()
```

### Linux Distribution Specific

#### **Ubuntu/Debian**

```bash
# Install dependencies
sudo apt-get install python3 python3-pip git

# Clone and install
git clone https://github.com/username/zapprobe.git
cd zapprobe
python3 linux_setup.py
```

#### **Fedora**

```bash
# Install dependencies
sudo dnf install python3 python3-pip git

# Clone and install
git clone https://github.com/username/zapprobe.git
cd zapprobe
python3 linux_setup.py
```

#### **Arch Linux**

```bash
# Install dependencies
sudo pacman -S python pip git

# Clone and install
git clone https://github.com/username/zapprobe.git
cd zapprobe
python3 linux_setup.py
```

### Linux Usage Examples

```bash
# Basic scan
zapprobe http://localhost:5000/search?id=1

# With custom delay (good for IDS evasion)
zapprobe http://localhost:5000/search?id=1 --delay 2

# With Burp Suite on Linux
zapprobe http://localhost:5000/search?id=1 --proxy http://127.0.0.1:8080

# Save to file (on Linux)
zapprobe http://localhost:5000/search?id=1 -o ~/report.html

# Multiple parameters
zapprobe "http://localhost:5000/search?id=1&name=test" -t all --timeout 30

# Run in background and save output
zapprobe http://localhost:5000/search?id=1 -o report.json &
```

---

## ⚠️ LEGAL DISCLAIMER

**THIS TOOL IS FOR EDUCATIONAL PURPOSES ONLY!**

- ✅ Use **ONLY** on your own systems
- ✅ Use **ONLY** in authorized test environments
- ✅ Obtain **written permission** before testing any server
- ❌ Unauthorized testing is **ILLEGAL**
- ❌ **NEVER** use on real websites without permission
- ❌ Use for malicious purposes is **PROHIBITED**

**⚖️ The developer is NOT responsible for misuse of this tool. Users are solely responsible for all legal consequences.**

## 📋 Features

- ✅ SQL Injection Detection (100+ payloads)
- ✅ XSS Detection (60+ payloads)
- ✅ GUI Interface (PySimpleGUI)
- ✅ Simple CLI (one-liner scans)
- ✅ JSON/HTML Reports
- ✅ Proxy Support (Burp Suite, ZAP)
- ✅ SSL Configuration
- ✅ CVSS Scoring
- ✅ Custom Delays & Timeouts

## 📋 In the future

- Improved payload detection engine

## 🔧 Options

```
-t, --type {sqli,xss,all}     Scan type (default: all)
--timeout SECONDS              Request timeout (default: 10)
--delay SECONDS               Delay between requests (default: 0.5)
--no-ssl-verify              Disable SSL verification
--proxy PROXY_URL            HTTP proxy (e.g., http://127.0.0.1:8080)
-o, --output FILE            Output file (JSON or HTML)
--gui                        Launch GUI mode
-v, --version                Show version
```

## ⚠️ Educational Purpose Only

This tool was developed strictly for educational and research purposes.  
It aims to help developers and security enthusiasts understand the mechanics of SQL Injection and Cross-Site Scripting (XSS) vulnerabilities.

Do not use this tool on systems without explicit permission.
