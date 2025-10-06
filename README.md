# ZapProbe Security Scanner

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-in%20development-yellow.svg)

An educational web vulnerability scanner for detecting SQL Injection and Cross-Site Scripting (XSS) vulnerabilities.

## ⚠️ LEGAL DISCLAIMER

**THIS TOOL IS FOR EDUCATIONAL PURPOSES ONLY!**

- ✅ Use **ONLY** on your own systems
- ✅ Use **ONLY** in authorized test environments
- ✅ Obtain **written permission** before testing any server
- ❌ Unauthorized testing is **ILLEGAL**
- ❌ **NEVER** use on real websites without permission
- ❌ Use for malicious purposes is **PROHIBITED**

**⚖️ The developer is NOT responsible for misuse of this tool. Users are solely responsible for all legal consequences.**

---

## 📋 Features

### 🎯 Currently Available:

- ✅ **SQL Injection Scanning**: Test with 30+ different SQLi payloads
- ✅ **XSS Scanning**: Detection of Reflected XSS vulnerabilities
- ✅ **Colorful Terminal Output**: Clear and readable results
- ✅ **Scan Reports**: Summary of discovered vulnerabilities
- ✅ **Rate Limiting**: Delay mechanism to reduce server load
- ✅ **Test Server**: Intentionally vulnerable sample application for learning

### 🚧 Under Development:

- 🔨 DOM-based XSS detection
- 🔨 Blind SQLi testing
- 🔨 JSON and XML format support
- 🔨 HTML/PDF report generation
- 🔨 POST method support
- 🔨 Cookie and header testing
- 🔨 Multi-threading support

---

## 📦 Installation

### Requirements:

- Python 3.8 or higher
- pip (Python package manager)

### Step-by-Step Installation:

```bash
# 1. Clone the repository
git clone https://github.com/username/simple-security-scanner.git
cd simple-security-scanner

# 2. Create a virtual environment (recommended)
python -m venv venv

# 3. Activate the virtual environment

# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt
```

---

## 🚀 Usage

### Basic Usage:

```bash
# SQL Injection and XSS scan (default)
python scanner.py -u "http://example.com/page?id=1"

# SQL Injection scan only
python scanner.py -u "http://example.com/page?id=1" -t sqli

# XSS scan only
python scanner.py -u "http://example.com/page?id=1" -t xss

# Change timeout duration
python scanner.py -u "http://example.com/page?id=1" --timeout 15
```

### Command Parameters:

```
-u, --url          Target URL (required)
-t, --type         Scan type: sqli, xss, all (default: all)
--timeout          Request timeout in seconds (default: 10)
-h, --help         Show help information
```

---

## 🧪 Test Server

The project includes an intentionally vulnerable test server for educational purposes.

### Start the Test Server:

```bash
# Install Flask (if not already installed)
pip install flask

# Run the test server
python examples/test_server.py
```

The server will run at `http://localhost:5000`

### Test Endpoints:

```bash
# Homepage
http://localhost:5000/

# SQL Injection test
http://localhost:5000/search?id=1

# XSS test
http://localhost:5000/comment?text=hello

# Login SQLi test
http://localhost:5000/login?username=admin&password=test
```

### Test with Scanner:

```bash
# Scan against test server
python scanner.py -u "http://localhost:5000/search?id=1"
```

---

## 📊 Sample Output

```
============================================================
SECURITY SCANNER - EDUCATIONAL TOOL
============================================================
WARNING: Use only on authorized targets!
============================================================

[i] Starting SQL Injection scan on http://localhost:5000/search?id=1
------------------------------------------------------------

[i] Testing parameter: id
[✗] SQLi vulnerability found with payload: '...
[✗] SQLi vulnerability found with payload: ' OR '1'='1...
[✗] SQLi vulnerability found with payload: ' OR '1'='1' --...

[i] Starting XSS scan on http://localhost:5000/search?id=1
------------------------------------------------------------

[i] Testing parameter: id
[✓] No XSS vulnerabilities detected

============================================================
SCAN SUMMARY
============================================================
Target URL: http://localhost:5000/search?id=1
Scan Time: 2025-01-15 14:30:45
Total Vulnerabilities Found: 3
============================================================

[✗] Vulnerability #1:
  Type: SQL Injection
  Payload: '
  Time: 14:30:46
------------------------------------------------------------
```

---

## 📁 Project Structure

```
simple-security-scanner/
├── scanner.py              # Main scanner program
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── LICENSE                # MIT License
├── payloads/              # Test payloads
│   ├── __init__.py
│   ├── sqli_payloads.py   # SQL Injection payloads
│   └── xss_payloads.py    # XSS payloads
├── utils/                 # Utility functions
│   ├── __init__.py
│   ├── colors.py          # Terminal colorization
│   └── reporter.py        # Report generator
└── examples/              # Test examples
    ├── __init__.py
    └── test_server.py     # Vulnerable test server
```

---

## 🔧 Technologies

- **Python 3.8+**: Main programming language
- **Requests**: For HTTP requests
- **BeautifulSoup4**: For HTML parsing
- **Colorama**: Colorful terminal output
- **Flask**: For test server (optional)

---

## 🎓 Educational Goals

This tool is designed to help you learn:

1. **Web Security Concepts**:

   - How SQL Injection vulnerabilities work
   - When XSS attacks occur
   - Why input validation is crucial

2. **Ethical Hacking Basics**:

   - How vulnerability scanners operate
   - Penetration testing methodology
   - Responsible Disclosure practices

3. **Python Programming**:
   - HTTP request handling
   - Command-line applications
   - Error handling and logging

---

## 🛡️ How to Protect Yourself

To protect against these vulnerabilities:

### For Developers:

- ✅ **Never** use user input directly in SQL queries
- ✅ Use **parametrized queries** or **prepared statements**
- ✅ **HTML encode** all outputs
- ✅ Implement **input validation** and **sanitization**
- ✅ Add **Content Security Policy (CSP)** headers

### Code Example (Secure):

```python
# ❌ WRONG (Vulnerable):
query = f"SELECT * FROM users WHERE id = {user_input}"

# ✅ CORRECT (Secure):
query = "SELECT * FROM users WHERE id = ?"
cursor.execute(query, (user_input,))
```

---

## 🤝 Contributing

Contributions are welcome! To improve the project:

1. **Fork** this repository
2. Create a new **branch** (`git checkout -b feature/NewFeature`)
3. **Commit** your changes (`git commit -m 'feat: add new feature'`)
4. **Push** the branch (`git push origin feature/NewFeature`)
5. Open a **Pull Request**

### Contribution Guidelines:

- Code must follow Python PEP 8 standards
- Add tests for new features
- Commit messages should be clear and descriptive
- Open an Issue first for major changes

---

## 📝 License

This project is distributed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🚧 Project Status

**⚠️ NOTICE: This project is currently under active development.**

### Current Status:

- ✅ Core functionality is working
- ✅ SQL Injection and XSS scanning available
- ✅ Test server is ready

### Planned Improvements:

- 🔨 More payload types
- 🔨 Advanced reporting features
- 🔨 GUI interface (Tkinter/PyQt)
- 🔨 Database support (save scan results)
- 🔨 Configuration file support
- 🔨 Plugin system
- 🔨 Docker containerization

### Known Limitations:

- ⚠️ GET requests only (POST support coming soon)
- ⚠️ Basic error handling (will be improved)
- ⚠️ Limited payload collection (will be expanded)

---

## 📚 Additional Resources

### Learn More:

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [HackerOne Hacktivity](https://hackerone.com/hacktivity)

### Similar Tools:

- [SQLMap](https://sqlmap.org/) - Advanced SQL injection tool
- [Burp Suite](https://portswigger.net/burp) - Professional testing suite
- [OWASP ZAP](https://www.zaproxy.org/) - Free security scanner

---

## 📞 Contact

- **GitHub Issues**: [Project Issues](https://github.com/username/simple-security-scanner/issues)
- **Author**: [Your Name]
- **Email**: your.email@example.com

---

## 🙏 Acknowledgments

This project was created for educational purposes and is supported by the open-source community.

Special thanks to:

- OWASP team for security education
- Python community for excellent libraries
- All contributors and testers

---

## ⭐ Support

If you find this project useful, don't forget to give it a star ⭐!

---

**Last Updated**: January 2025  
**Version**: 0.1.0 (Alpha)  
**Status**: 🚧 Active Development

---

<div align="center">
  
**🔒 Use Responsibly. Learn. Improve. Share. 🔒**

Made with ❤️ for Cybersecurity Education

</div>
