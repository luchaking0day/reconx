# 🔍 ReconX - Domain & IP OSINT Reconnaissance Tool

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square&logo=python" />
  <img src="https://img.shields.io/badge/platform-Linux%20%7C%20Kali-green?style=flat-square" />
  <img src="https://img.shields.io/badge/license-MIT-orange?style=flat-square" />
  <img src="https://img.shields.io/badge/OSINT-tool-red?style=flat-square" />
</p>

> A modular, CLI-based OSINT reconnaissance tool for domains and IP addresses.  
> Built for security researchers, CTF players and penetration testers.

---

## Features

| Module | Description |
|--------|-------------|
| 🔎 **WHOIS** | Registrar, registrant, dates, name servers, DNSSEC |
| 🌐 **DNS Enum** | A, AAAA, MX, NS, TXT, CNAME, SOA, CAA, PTR records |
| 🔗 **Subdomain Scan** | Brute-force via customizable wordlist, multi-threaded |
| 🚪 **Port Scan** | Top 100 ports, banner grabbing, service detection |
| 💾 **JSON Output** | Save full results to structured JSON file |

---

## Installation

```bash
# Clone the repo
git clone https://github.com/luchaking0day/reconx.git
cd reconx

# Make executable
chmod +x reconx.py

# Install globally (allows running 'reconx' from anywhere)
sudo cp reconx.py /usr/local/bin/reconx

# No pip install needed — uses Python standard library only
# Optional: install whois and dnsutils for best results
sudo apt install whois dnsutils

# Run all modules
reconx example.com

# Run specific modules
reconx example.com -w -d           # WHOIS + DNS
reconx example.com -s              # Subdomains only
reconx example.com -p              # Ports only

# Save output to JSON
reconx example.com -a -o results/example.json

# Custom wordlist + more ports
reconx example.com -s --wordlist /usr/share/wordlists/subdomains.txt
reconx example.com -p --top-ports 200 --timeout 0.5

Compatibility
✅ Kali Linux (recommended)

✅ Ubuntu / Debian

✅ macOS (without dig/whois fallback to socket)

✅ Python 3.10+

❌ Windows (not tested)

Disclaimer
This tool is intended for educational purposes and authorized penetration testing only.

Always obtain proper written permission before scanning systems you do not own.

The author is not responsible for any misuse or damage caused by this tool.

License
MIT License — see LICENSE for details.





