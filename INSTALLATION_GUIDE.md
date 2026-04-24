# 📦 ZapProbe - Cross-Operating System Installation Summary

## 🎯 Fast Installation For Any OS

### Linux ✅

```bash
cd zapprobe
python3 linux_setup.py --gui
zapprobe --gui
```

### macOS ✅

```bash
cd zapprobe
chmod +x install_macos.sh
./install_macos.sh
zapprobe --gui
```

### Windows ✅

```bash
cd zapprobe
install_windows.bat
zapprobe --gui
```

---

## 📁 New File Structure

```
ZapProbe/
├── scanner.py                 # Main scanner module
├── cli_runner.py             # GUI + CLI integration (NEW)
├── linux_setup.py            # Linux automatic installation (NEW)
├── install_windows.bat       # Windows Setup Script (NEW)
├── install_macos.sh          # macOS installation script (NEW)
├── LINUX_GUIDE.md            # Linux Detailed Guide (NEW)
├── README.md                 # Updated
├── setup.py                  # Updated
├── requirements.txt          # Updated
├── payloads/
│   ├── sqli_payloads.py      # 100+ SQL injection payloads
│   └── xss_payloads.py       # 60+ XSS payloads
├── utils/
│   ├── colors.py             # Terminal colors
│   └── reporter.py           # JSON/HTML report
├── examples/
│   └── test_server.py        # Vulnerable test server
└── zapprobe.egg-info/
```

---

## 🌐 Operating System Comparison

| Feature           | Linux                    | macOS                | Windows               |
| ----------------- | ------------------------ | -------------------- | --------------------- |
| **Setup**         | `python3 linux_setup.py` | `./install_macos.sh` | `install_windows.bat` |
| **Command**       | `zapprobe`               | `zapprobe`           | `zapprobe`            |
| **GUI**           | ✅ PySimpleGUI           | ✅ PySimpleGUI       | ✅ PySimpleGUI        |
| **Test Server**   | ✅ Flask                 | ✅ Flask             | ✅ Flask              |
| **Proxy Support** | ✅ Burp/ZAP              | ✅ Burp/ZAP          | ✅ Burp/ZAP           |
| **SSL Verify**    | ✅ Configurable          | ✅ Configurable      |
| ✅ Configurable   |

---

## 🔧 3 Usage Modes (Across All OSs)

### 1️⃣ GUI Mode (Graphical Interface)

```bash
zapprobe --gui
```

- ✅ The easiest
- ✅ For beginner users
- ✅ All options are visual.

### 2️⃣ Quick CLI (Fast)

```bash
zapprobe http://localhost:5000/search?id=1
```

- ✅ Single-line scan
- ✅ Default options

### 3️⃣ Advanced CLI (Controlled)

```bash
zapprobe http://target.com/page?id=1 \
  -t all \
  --timeout 30 \
  --proxy http://127.0.0.1:8080 \
  -o report.html
```

- ✅ All options
- ✅ For advanced users

---

## 📚 Guides

### Linux Users

👉 [LINUX_GUIDE.md](LINUX_GUIDE.md)

**Includes:**

- System requirements
- Automatic installation
- Detailed troubleshooting
- Distribution-specific guides
- Linux tips

### macOS Users

👉 [README.md](README.md) - macOS section

**Steps:**

1. `install_macos.sh` run
2. `zapprobe --gui` run the command
3. Set up proxy (optional)

### Windows Users

👉 [README.md](README.md) - Windows section

**Steps:**

1. `install_windows.bat` run
2. `zapprobe --gui` run the command
3. Install PySimpleGUI (optional)

---

## ⚡ Quick Start (Linux Example)

```bash
# 1. Download
git clone https://github.com/username/zapprobe.git
cd zapprobe

# 2. Create
python3 linux_setup.py --gui

# 3. Use
zapprobe --gui
# or
zapprobe http://localhost:5000/search?id=1

# 4. Test with the test server
python3 examples/test_server.py &
zapprobe http://localhost:5000/search?id=1 -o report.html
```

---

## 🐛 Troubleshooting

| Problem                       | Solution                                    |
| ----------------------------- | ------------------------------------------- |
| `command not found: zapprobe` | `python3 -m cli_runner` `pip3 install -e .` |
| `ImportError: requests`       | `pip3 install -r requirements.txt`          |
| `Port already in use`         | `lsof -i :5000` and close the process       |
| `SSL certificate error`       | `--no-ssl-verify` use flag                  |
| `PySimpleGUI not found`       | `pip install PySimpleGUI`                   |

---

## 📝 Post-Installation Steps

```bash
# Established locations
Linux:   ~/.local/bin/zapprobe
macOS:   /usr/local/bin/zapprobe
Windows: %APPDATA%\Python\Scripts\zapprobe.exe

# Or as a Python module
python3 -m cli_runner [OPTIONS]
```

---

## 🎁 Innovations

### v0.3.0

- ✅ GUI Interface (PySimpleGUI)
- ✅ Automatic installation scripts
- ✅ Linux/macOS/Windows support
- ✅ Detailed guides
- ✅ Improved CLI

### v0.2.0

- ✅ POST request support
- ✅ Proxy support
- ✅ JSON/HTML report
- ✅ CVSS Scoring
- ✅ 100+ SQLi payloads

### v0.1.0

- ✅ Basic SQLi/XSS scanning

---

## 🚀 Next Steps

1. **Install:** `python3 linux_setup.py` (Linux) or `install_macos.sh` (macOS)
2. **Test:** `zapprobe --gui`
3. **Read Documentation:** [LINUX_GUIDE.md](LINUX_GUIDE.md)
4. **Found a Bug?** Report it in GitHub Issues

---

**Having any problems? Check the Troubleshooting section in [LINUX_GUIDE.md](LINUX_GUIDE.md)!** 🔧
