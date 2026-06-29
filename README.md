# ⚡ ASTRA-SECURE CCTV INTELLIGENCE SUITE v2.0

## Developed by SMILE for ASTRA TECH

### 🚀 Overview

ASTRA-SECURE is a professional-grade network security auditing tool designed to assess the vulnerability of IP-based CCTV surveillance systems. It combines network scanning, port detection, and credential testing in a single, elegant framework.

### 🎯 Features

- **Multi-Manufacturer Support**: Hikvision, Dahua, Axis, TP-Link, and 50+ others
- **Intelligent Detection**: Identifies camera models from HTTP headers and port patterns
- **Credential Brute Force**: Tests 8,000+ default credentials
- **RTSP Stream Discovery**: Finds live streaming URLs when credentials are valid
- **Auto-Installation**: One-command setup for Termux
- **JSON/HTML Reports**: Exports all discovered information
- **Real-time Progress**: Animated scanning progress bars
- **Cross-Platform**: Works on Termux, Kali, Ubuntu, Windows (WSL)

### 📦 Installation

```bash
# Clone the repository
git clone https://github.com/darkdev-tech/Cctv-.git
cd Cctv

# For Termux (Android)
bash INSTALL.sh

# For Linux (Kali/Ubuntu)
sudo apt update
sudo apt install python3 python3-pip git nmap
pip3 install -r requirements.txt
