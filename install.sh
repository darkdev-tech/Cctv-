#!/bin/bash
#########################################################
# ASTRA-SECURE CCTV Intelligence Suite v2.0
# Developed by SMILE for ASTRA TECH
# INSTALLATION SCRIPT
#########################################################

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║          ASTRA-SECURE CCTV INTELLIGENCE SUITE               ║"
echo "║                    INSTALLATION SCRIPT                      ║"
echo "║               DEVELOPED BY SMILE FOR ASTRA TECH             ║"
echo "╚══════════════════════════════════════════════════════════════╝"

echo ""
echo "[+] Updating package repositories..."
pkg update -y && pkg upgrade -y

echo "[+] Installing required packages..."
pkg install -y python python-pip git wget nmap openssh

echo "[+] Installing Python dependencies..."
pip install -r requirements.txt

echo "[+] Setting up directories..."
mkdir -p scan_results
mkdir -p reports

echo "[+] Configuring permissions..."
chmod +x astra_cctv_scanner.py

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║           INSTALLATION COMPLETE!                           ║"
echo "║                                                           ║"
echo "║  To run:  python3 astra_cctv_scanner.py                   ║"
echo "║                                                           ║"
echo "║  ⚠️  REMEMBER: FOR EDUCATIONAL USE ONLY                   ║"
echo "║  Unauthorized access is a federal crime                   ║"
echo "║                                                           ║"
echo "║         🔒 SECURE. LEARN. PROTECT. 🔒                     ║"
echo "║                    ASTRA TECH | SMILE                     ║"
echo "╚══════════════════════════════════════════════════════════════╝"
