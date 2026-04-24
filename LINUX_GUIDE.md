# 🐧 ZapProbe - Linux Users Complete Guide

**English Guide: Installing and using ZapProbe on Linux**

---

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Testing](#testing)
5. [Troubleshooting](#troubleshooting)
6. [Linux Distribution Specific](#linux-distribution-specific)

---

## System Requirements

### Check Minimum Requirements

```bash
# Python version (3.8+ required)
python3 --version

# pip version
pip3 --version

# git (for cloning)
git --version
```

**If missing:**

| Distribution  | Installation Command                           |
| ------------- | ---------------------------------------------- |
| Ubuntu/Debian | `sudo apt-get install python3 python3-pip git` |
| Fedora        | `sudo dnf install python3 python3-pip git`     |
| Arch          | `sudo pacman -S python pip git`                |
| macOS         | `brew install python3 git`                     |

---

## Installation

### Step 1: Download the Project

```bash
# Clone from GitHub
git clone https://github.com/username/zapprobe.git
cd zapprobe

# Or download ZIP and extract
# unzip zapprobe.zip
# cd zapprobe
```

### Step 2: Automatic Installation (Recommended)

```bash
# Basic installation
python3 linux_setup.py

# With GUI support
python3 linux_setup.py --gui
```

**This command will automatically:**

- Check Python 3.8+
- Check pip
- Install all dependencies
- Install package globally
- Test the installation

### Step 3: Manual Installation (Alternative)

```bash
# Install dependencies
pip3 install -r requirements.txt

# Add GUI support (optional)
pip3 install PySimpleGUI

# Install the package
pip3 install -e .

# Test the installation
zapprobe --version
```

### Step 4: Verify Successful Installation

```bash
# zapprobe command should work
zapprobe --help

# Or as a Python module
python3 -m cli_runner --help
```

---

## Quick Start

### 3 Usage Methods

#### 1️⃣ **GUI Mode (Easiest)**

```bash
zapprobe --gui
```

✅ Graphical interface opens
✅ All options are visible
✅ Click and run with mouse

#### 2️⃣ **Quick CLI (Fastest)**

```bash
# Single-line scan
zapprobe http://target.com/page?id=1
```

✅ Enter the URL
✅ Press Enter
✅ Scan starts

#### 3️⃣ **Advanced CLI (Most Control)**

```bash
# With all options
zapprobe http://target.com/page?id=1 \
  -t all \
  --timeout 30 \
  --delay 1 \
  --proxy http://127.0.0.1:8080 \
  -o report.html
```

---

## Testing

### Scenario 1: Test with Vulnerable Server

#### Terminal 1: Start the Test Server

```bash
# Go to ZapProbe directory
cd ~/zapprobe

# Run the test server
python3 examples/test_server.py
```

**Output:**

```
======================================================================
🚨 VULNERABLE TEST SERVER - EDUCATIONAL USE ONLY
======================================================================

📍 Server starting on http://localhost:5000

📋 Test endpoints:
  - GET:  http://localhost:5000/
  - GET:  http://localhost:5000/search?id=1
  ...
```

✅ Server is running (keep this tab open)

#### Terminal 2: Run the Scanner

```bash
# Open a new terminal

# SQL Injection Test
zapprobe http://localhost:5000/search?id=1 -t sqli

# XSS Test
zapprobe http://localhost:5000/comment?text=test -t xss

# Full Scan
zapprobe http://localhost:5000/search?id=1

# With HTML Report
zapprobe http://localhost:5000/search?id=1 -o report.html
```

#### Open the Report

```bash
# Open HTML report
firefox report.html          # Linux
open report.html             # macOS

# Or view as JSON
cat report.json | less
```

---

### Scenario 2: Test with Burp Suite

#### 1. Start Burp Suite

```bash
# If Burp Suite is installed on Linux
burp

# Or manually
java -jar burpsuite_community.jar
```

#### 2. Proxy Settings

- Proxy → Options
- Port: `8080`
- Checked: "Running"

#### 3. Scan with ZapProbe

```bash
# Use Burp Suite proxy
zapprobe http://localhost:5000/search?id=1 \
  --proxy http://127.0.0.1:8080

# All requests will be visible in Burp
```

---

### Scenario 3: Remote Server Test

```bash
# Real target (with authorization)
zapprobe https://target.example.com/search?id=1 \
  --timeout 30 \
  --delay 2 \
  -o ~/Desktop/target_report.html

# If SSL error occurs
zapprobe https://target.example.com/search?id=1 \
  --no-ssl-verify
```

---

## Troubleshooting

### Identifying and Solving Issues

#### ❌ Issue: "command not found: zapprobe"

**Cause:** Command not found in PATH

**Solution:**

```bash
# Step 1: Check where it's installed
which zapprobe
ls -la ~/.local/bin/zapprobe

# Step 2: Run the module directly
python3 -m cli_runner --version

# Step 3: Fix PATH
# Open ~/.bashrc file
nano ~/.bashrc

# Add to the end
export PATH="$PATH:$HOME/.local/bin"

# Save (Ctrl+O, Enter, Ctrl+X)
# Reload terminal
source ~/.bashrc

# Try again
zapprobe --version
```

---

#### ❌ Issue: "ImportError: No module named 'requests'"

**Cause:** Dependencies are not installed

**Solution:**

```bash
# Step 1: Check requirements.txt
ls -la requirements.txt

# Step 2: Install dependencies
pip3 install -r requirements.txt

# Step 3: Or one by one
pip3 install requests beautifulsoup4 colorama urllib3

# Step 4: Test
python3 -c "import requests; print('OK')"
```

---

#### ❌ Issue: "Port 5000 already in use"

**Cause:** Another application is using port 5000

**Solution:**

```bash
# Step 1: Which process is using it?
lsof -i :5000

# Step 2: Kill the process
kill -9 <PID>

# Step 3: Use a different port (edit test_server.py)
# Find line 343:
# app.run(debug=True, host='127.0.0.1', port=5000)
# Change to:
# app.run(debug=True, host='127.0.0.1', port=5001)

nano examples/test_server.py
# Change port 5000 → 5001
# Ctrl+O, Enter, Ctrl+X

# Step 4: Restart
python3 examples/test_server.py  # Will run on port 5001
```

---

#### ❌ Issue: "Permission denied" when running test_server.py

**Cause:** File is not executable

**Solution:**

```bash
# Step 1: Give the file executable permission
chmod +x examples/test_server.py

# Step 2: Or run with Python
python3 examples/test_server.py

# Step 3: Or directly
./examples/test_server.py   # Requires #!/usr/bin/env python3 in header
```

---

#### ❌ Issue: "SSL: CERTIFICATE_VERIFY_FAILED"

**Cause:** SSL certificate could not be verified

**Solution:**

```bash
# Step 1: Add flag
zapprobe https://localhost:5443/search?id=1 \
  --no-ssl-verify

# Step 2: Or set environment variable
export PYTHONHTTPSVERIFY=0
zapprobe https://localhost:5443/search?id=1

# Step 3: Permanent solution - install certificate
# (Preferred in production environments)
```

---

#### ❌ Issue: "ModuleNotFoundError: No module named 'PySimpleGUI'"

**Cause:** Optional dependency for GUI is not installed

**Solution:**

```bash
# Step 1: Install PySimpleGUI
pip3 install PySimpleGUI

# Step 2: Or continue from setup
pip3 install -e ".[gui]"

# Step 3: Test
zapprobe --gui
```

---

#### ❌ Issue: "Connection refused" localhost:5000

**Cause:** Test server is not running

**Solution:**

```bash
# Step 1: Check if server is started
ps aux | grep "test_server.py"

# Step 2: If not, start it
python3 examples/test_server.py

# Step 3: Check if port is open
netstat -tulpn | grep 5000
# or
ss -tulpn | grep 5000

# Step 4: Test with curl
curl http://localhost:5000/
```

---

## Linux Distribution Specific

### Ubuntu / Debian

```bash
# Update your system
sudo apt-get update
sudo apt-get upgrade

# ZapProbe installation
git clone https://github.com/username/zapprobe.git
cd zapprobe
python3 linux_setup.py --gui

# Use
zapprobe --gui
```

**If pip error:**

```bash
# Install Python 3 pip
sudo apt-get install python3-pip

# Or install pip manually
sudo apt-get install curl
curl https://bootstrap.pypa.io/get-pip.py | sudo python3
```

---

### Fedora / RHEL / CentOS

```bash
# Update your system
sudo dnf update

# ZapProbe installation
git clone https://github.com/username/zapprobe.git
cd zapprobe
python3 linux_setup.py --gui

# Use
zapprobe --gui
```

**If flask error:**

```bash
# Install development tools
sudo dnf groupinstall "Development Tools"
sudo dnf install python3-devel
```

---

### Arch Linux

```bash
# Update your system
sudo pacman -Syu

# ZapProbe installation
git clone https://github.com/username/zapprobe.git
cd zapprobe
python3 linux_setup.py --gui

# Use
zapprobe --gui
```

**Everything on Arch should be latest - issues are rare**

---

### macOS (Linux-like)

```bash
# Install Python with Homebrew
brew install python3

# ZapProbe installation
git clone https://github.com/username/zapprobe.git
cd zapprobe
python3 linux_setup.py --gui

# Use
zapprobe --gui

# Open HTML report
open report.html
```

---

## Linux Tips

### Performance Optimization

```bash
# Multi-thread support is planned, current solution:
zapprobe http://target.com/page?id=1 &   # Run in background
# Or
nohup zapprobe http://target.com/page?id=1 > scan.log &
```

### Logging

```bash
# Save output to file
zapprobe http://target.com/page?id=1 2>&1 | tee scan.log

# Or directly
zapprobe http://target.com/page?id=1 -o report.html > scan.log 2>&1
```

### Scheduled Scanning

```bash
# Add scan to crontab
crontab -e

# Add (every day at 2:00 AM)
0 2 * * * /usr/local/bin/zapprobe http://localhost:5000/search?id=1 -o ~/scans/daily_report.html
```

---

## Contact and Support

- **GitHub Issues:** Report bugs and ask questions
- **Documentation:** Check README.md
- **Community:** Join the discussion

---

**Questions? Remember nothing is perfect - use this for educational purposes!** 🚀
