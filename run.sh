#!/bin/bash
#########################################################
# ASTRA-SECURE CCTV Intelligence Suite v2.0
# Quick Launch Script
#########################################################

clear
echo "═══════════════════════════════════════════════════════════════"
echo "                    🚀 ASTRA TECH PRESENTS 🚀"
echo "                    DEVELOPED BY: SMILE"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "     █████╗ ███████╗████████╗██████╗  █████╗                 "
echo "    ██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔══██╗                "
echo "    ███████║███████╗   ██║   ██████╔╝███████║                "
echo "    ██╔══██║╚════██║   ██║   ██╔══██╗██╔══██║                "
echo "    ██║  ██║███████║   ██║   ██║  ██║██║  ██║                "
echo "    ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝                "
echo ""
echo "     ███████╗███████╗ ██████╗██╗   ██╗██████╗ ███████╗       "
echo "     ██╔════╝██╔════╝██╔════╝██║   ██║██╔══██╗██╔════╝       "
echo "     ███████╗█████╗  ██║     ██║   ██║██████╔╝█████╗         "
echo "     ╚════██║██╔══╝  ██║     ██║   ██║██╔══██╗██╔══╝         "
echo "     ███████║███████╗╚██████╗╚██████╔╝██║  ██║███████╗       "
echo "     ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝       "
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "              CCTV INTELLIGENCE SUITE v2.0"
echo "              DEVELOPED BY SMILE FOR ASTRA TECH"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "  ⚠️  LEGAL WARNING: FOR AUTHORIZED TESTING ONLY ⚠️"
echo "  Unauthorized access is a federal crime."
echo "  Use only on networks you own or have explicit permission."
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[!] Python3 not found! Installing..."
    pkg install python3 -y
fi

# Check if script exists
if [ ! -f "astra_cctv_scanner.py" ]; then
    echo "[!] Main script not found!"
    echo "[!] Please ensure astra_cctv_scanner.py is in the current directory"
    exit 1
fi

echo "[+] Launching ASTRA-SECURE Suite..."
echo ""
python3 astra_cctv_scanner.py
