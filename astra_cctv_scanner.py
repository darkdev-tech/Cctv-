#!/usr/bin/env python3
"""
ASTRA-SECURE CCTV Intelligence Suite v2.0
Developed by SMILE for ASTRA TECH
FOR EDUCATIONAL AND AUTHORIZED TESTING ONLY
"""

import socket
import sys
import os
import time
import json
import threading
import subprocess
from datetime import datetime
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# ============== CONFIGURATION ==============
VERSION = "2.0"
AUTHOR = "SMILE"
BRAND = "ASTRA TECH"
BANNER = f"""
{Fore.CYAN}
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║     █████╗ ███████╗████████╗██████╗  █████╗                 ║
    ║    ██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔══██╗                ║
    ║    ███████║███████╗   ██║   ██████╔╝███████║                ║
    ║    ██╔══██║╚════██║   ██║   ██╔══██╗██╔══██║                ║
    ║    ██║  ██║███████║   ██║   ██║  ██║██║  ██║                ║
    ║    ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝                ║
    ║                                                              ║
    ║     ███████╗███████╗ ██████╗██╗   ██╗██████╗ ███████╗       ║
    ║     ██╔════╝██╔════╝██╔════╝██║   ██║██╔══██╗██╔════╝       ║
    ║     ███████╗█████╗  ██║     ██║   ██║██████╔╝█████╗         ║
    ║     ╚════██║██╔══╝  ██║     ██║   ██║██╔══██╗██╔══╝         ║
    ║     ███████║███████╗╚██████╗╚██████╔╝██║  ██║███████╗       ║
    ║     ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝       ║
    ║                                                              ║
    ║          CCTV INTELLIGENCE SUITE v{VERSION}                     ║
    ║          DEVELOPED BY {AUTHOR} FOR {BRAND}                     ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
{Fore.YELLOW}
    ⚠️  LEGAL WARNING: FOR AUTHORIZED TESTING ONLY ⚠️
    Unauthorized access is a federal crime.
    Use only on networks you own or have explicit permission.
{Fore.RESET}
"""

# Camera manufacturer signatures
CAMERA_SIGNATURES = {
    "hikvision": {
        "ports": [80, 554, 8000, 8080],
        "default_creds": [("admin", "12345"), ("admin", "admin"), ("admin", "hik12345")],
        "model_patterns": ["DS-2", "DS-6", "iDS-2"]
    },
    "dahua": {
        "ports": [80, 554, 37777, 8080],
        "default_creds": [("admin", "admin"), ("admin", "123456"), ("admin", "dahua")],
        "model_patterns": ["DHI-", "IPC-", "DH-"]
    },
    "axis": {
        "ports": [80, 554, 8080, 443],
        "default_creds": [("root", "pass"), ("root", "admin"), ("admin", "admin")],
        "model_patterns": ["AXIS", "P32", "Q60"]
    },
    "tp-link": {
        "ports": [80, 554, 2020, 8080],
        "default_creds": [("admin", "admin"), ("admin", "12345"), ("admin", "password")],
        "model_patterns": ["NC", "TL-IPC", "Tap"]
    },
    "generic": {
        "ports": [80, 554, 8080],
        "default_creds": [("admin", "admin"), ("admin", "12345"), ("admin", "password")],
        "model_patterns": []
    }
}

# ============== CORE FUNCTIONS ==============

def show_banner():
    """Display the ASTRA TECH banner"""
    os.system('clear' if os.name == 'posix' else 'cls')
    print(BANNER)

def validate_ip(ip):
    """Validate IP address format"""
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit():
            return False
        num = int(part)
        if num < 0 or num > 255:
            return False
    return True

def port_scan(ip, ports):
    """Scan specified ports on target IP"""
    open_ports = []
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    return open_ports

def get_hostname(ip):
    """Get hostname from IP"""
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return "Unknown"

def detect_camera_type(ip, open_ports, http_response=""):
    """Detect camera manufacturer based on ports and response"""
    for cam_type, signature in CAMERA_SIGNATURES.items():
        # Check port matches
        matches = sum(1 for p in signature["ports"] if p in open_ports)
        if matches >= 2:  # At least 2 matching ports
            return cam_type
        
        # Check HTTP response for model patterns
        if http_response:
            for pattern in signature["model_patterns"]:
                if pattern in http_response:
                    return cam_type
    
    return "generic"

def test_credentials(ip, port, username, password):
    """Test credentials on RTSP or HTTP port"""
    # RTSP authentication test
    if port == 554:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect((ip, port))
            # Base64 encode credentials for Basic Auth
            import base64
            creds = f"{username}:{password}"
            encoded = base64.b64encode(creds.encode()).decode()
            auth_header = f"DESCRIBE rtsp://{ip}:{port}/ RTSP/1.0\r\nCSeq: 1\r\nAuthorization: Basic {encoded}\r\n\r\n"
            sock.send(auth_header.encode())
            response = sock.recv(1024).decode()
            sock.close()
            if "200 OK" in response:
                return True
        except:
            pass
    return False

def brute_force_credentials(ip, open_ports):
    """Attempt to brute force credentials on discovered ports"""
    results = []
    for port in open_ports:
        if port in [80, 554, 8080, 443, 8000, 37777]:
            for cam_type, signature in CAMERA_SIGNATURES.items():
                for username, password in signature["default_creds"]:
                    if test_credentials(ip, port, username, password):
                        results.append({
                            "ip": ip,
                            "port": port,
                            "username": username,
                            "password": password,
                            "camera_type": cam_type
                        })
                        return results  # Return on first success
    return results

def scan_network(ip_range):
    """Main network scanning function"""
    results = []
    base_ip = ".".join(ip_range.split(".")[:-1])
    start = 1
    end = 254
    
    # Parse range if specified (e.g., 192.168.1.1-50)
    if "-" in ip_range:
        parts = ip_range.split("-")
        base_ip = ".".join(parts[0].split(".")[:-1])
        start = int(parts[0].split(".")[-1])
        end = int(parts[1]) if parts[1].isdigit() else 254
    
    total = end - start + 1
    current = 0
    
    print(f"\n{Fore.GREEN}➜ Scanning network: {base_ip}.{start}-{end}")
    print(f"{Fore.YELLOW}➜ Total targets: {total}")
    print(f"{Fore.CYAN}➜ Starting scan...{Fore.RESET}\n")
    
    for i in range(start, end + 1):
        ip = f"{base_ip}.{i}"
        current += 1
        progress = (current / total) * 100
        
        # Show progress
        bar_length = 50
        filled = int(bar_length * current // total)
        bar = '█' * filled + '░' * (bar_length - filled)
        print(f"\r{Fore.CYAN}[{bar}] {progress:.1f}% - Scanning {ip}   ", end="")
        
        # Check if host is up
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((ip, 80))
            sock.close()
            if result != 0:
                continue
        except:
            continue
        
        # Port scan common CCTV ports
        all_ports = [80, 554, 8080, 443, 8000, 37777, 8554, 2020, 5050, 7000]
        open_ports = port_scan(ip, all_ports)
        
        if open_ports:
            print(f"\n{Fore.GREEN}✓ Found device: {ip}")
            print(f"{Fore.BLUE}  ➜ Open ports: {open_ports}")
            
            # Detect camera type
            cam_type = detect_camera_type(ip, open_ports)
            print(f"{Fore.YELLOW}  ➜ Detected: {cam_type.upper()}")
            
            # Get hostname
            hostname = get_hostname(ip)
            print(f"{Fore.WHITE}  ➜ Hostname: {hostname}")
            
            # Try credential brute force
            creds = brute_force_credentials(ip, open_ports)
            if creds:
                for cred in creds:
                    print(f"{Fore.GREEN}  ➜ CREDENTIALS FOUND: {cred['username']}:{cred['password']}")
                    print(f"{Fore.GREEN}  ➜ RTSP URL: rtsp://{cred['username']}:{cred['password']}@{ip}:{cred['port']}/stream")
            else:
                print(f"{Fore.RED}  ➜ No default credentials found")
            
            # Save result
            results.append({
                "ip": ip,
                "hostname": hostname,
                "ports": open_ports,
                "camera_type": cam_type,
                "credentials": creds,
                "timestamp": datetime.now().isoformat()
            })
            print("")
    
    print(f"\n{Fore.GREEN}✓ Scan complete! Found {len(results)} devices.{Fore.RESET}")
    return results

def save_results(results):
    """Save scan results to files"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save JSON report
    json_file = f"astra_scan_{timestamp}.json"
    with open(json_file, "w") as f:
        json.dump(results, f, indent=2)
    
    # Save readable report
    txt_file = f"astra_scan_{timestamp}.txt"
    with open(txt_file, "w") as f:
        f.write("=" * 70 + "\n")
        f.write(f"ASTRA-SECURE CCTV SCAN REPORT\n")
        f.write(f"Developed by SMILE for ASTRA TECH\n")
        f.write(f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 70 + "\n\n")
        
        for result in results:
            f.write(f"IP Address: {result['ip']}\n")
            f.write(f"Hostname: {result['hostname']}\n")
            f.write(f"Camera Type: {result['camera_type']}\n")
            f.write(f"Open Ports: {result['ports']}\n")
            
            if result['credentials']:
                for cred in result['credentials']:
                    f.write(f"CREDENTIALS: {cred['username']}:{cred['password']}\n")
                    f.write(f"RTSP URL: rtsp://{cred['username']}:{cred['password']}@{result['ip']}:{cred['port']}/stream\n")
            else:
                f.write("No credentials found\n")
            f.write("-" * 50 + "\n")
    
    print(f"\n{Fore.GREEN}✓ Results saved to:")
    print(f"  ➜ {json_file}")
    print(f"  ➜ {txt_file}{Fore.RESET}")

def check_dependencies():
    """Check and install required Python packages"""
    required = ["colorama"]
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"{Fore.YELLOW}📦 Installing missing dependencies: {missing}")
        for package in missing:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"{Fore.GREEN}✓ Dependencies installed successfully!{Fore.RESET}")
        return True
    return True

def main_menu():
    """Display main menu interface"""
    while True:
        show_banner()
        print(f"{Fore.CYAN}┌──────────────────────────────────────────────┐")
        print(f"│              MAIN MENU                       │")
        print(f"├──────────────────────────────────────────────┤")
        print(f"│  {Fore.GREEN}1.{Fore.WHITE}  Scan IP Range (e.g., 192.168.1.1-50)│")
        print(f"│  {Fore.GREEN}2.{Fore.WHITE}  Scan Single IP                      │")
        print(f"│  {Fore.GREEN}3.{Fore.WHITE}  Load Saved Scan Results             │")
        print(f"│  {Fore.GREEN}4.{Fore.WHITE}  View System Information             │")
        print(f"│  {Fore.GREEN}5.{Fore.WHITE}  About ASTRA TECH                    │")
        print(f"│  {Fore.RED}6.{Fore.WHITE}  Exit                                 │")
        print(f"└──────────────────────────────────────────────┘")
        
        choice = input(f"\n{Fore.YELLOW}➜ Select option: {Fore.RESET}")
        
        if choice == "1":
            ip_range = input(f"{Fore.CYAN}➜ Enter IP range (e.g., 192.168.1.1-50 or 192.168.1.0/24): {Fore.RESET}")
            if ip_range:
                results = scan_network(ip_range)
                if results:
                    save_results(results)
                input(f"\n{Fore.CYAN}Press Enter to continue...{Fore.RESET}")
        
        elif choice == "2":
            ip = input(f"{Fore.CYAN}➜ Enter single IP (e.g., 192.168.1.100): {Fore.RESET}")
            if ip and validate_ip(ip):
                results = scan_network(ip)
                if results:
                    save_results(results)
                input(f"\n{Fore.CYAN}Press Enter to continue...{Fore.RESET}")
            else:
                print(f"{Fore.RED}✗ Invalid IP address{Fore.RESET}")
                time.sleep(2)
        
        elif choice == "3":
            import glob
            files = glob.glob("astra_scan_*.json")
            if files:
                print(f"\n{Fore.CYAN}Available reports:")
                for i, file in enumerate(files, 1):
                    print(f"  {Fore.GREEN}{i}.{Fore.WHITE} {file}")
                choice2 = input(f"{Fore.YELLOW}➜ Select report number: {Fore.RESET}")
                try:
                    idx = int(choice2) - 1
                    if 0 <= idx < len(files):
                        with open(files[idx], "r") as f:
                            data = json.load(f)
                            print(f"\n{Fore.GREEN}✓ Loaded {files[idx]}")
                            print(f"{Fore.CYAN}Found {len(data)} devices{Fore.RESET}")
                            for device in data:
                                print(f"\n{Fore.WHITE}IP: {device['ip']}")
                                print(f"Type: {device['camera_type']}")
                                if device['credentials']:
                                    for cred in device['credentials']:
                                        print(f"Credentials: {cred['username']}:{cred['password']}")
                            input(f"\n{Fore.CYAN}Press Enter to continue...{Fore.RESET}")
                    else:
                        print(f"{Fore.RED}✗ Invalid selection{Fore.RESET}")
                        time.sleep(2)
                except:
                    print(f"{Fore.RED}✗ Invalid input{Fore.RESET}")
                    time.sleep(2)
            else:
                print(f"{Fore.YELLOW}✗ No saved reports found{Fore.RESET}")
                time.sleep(2)
        
        elif choice == "4":
            import platform
            print(f"\n{Fore.CYAN}┌──────────────────────────────────────────────┐")
            print(f"│            SYSTEM INFORMATION                │")
            print(f"├──────────────────────────────────────────────┤")
            print(f"│  OS: {platform.system()} {platform.release()}")
            print(f"│  Python: {sys.version.split()[0]}")
            print(f"│  Scanner Version: {VERSION}")
            print(f"│  Developer: {AUTHOR}")
            print(f"│  Brand: {BRAND}")
            print(f"└──────────────────────────────────────────────┘")
            input(f"\n{Fore.CYAN}Press Enter to continue...{Fore.RESET}")
        
        elif choice == "5":
            print(f"\n{Fore.CYAN}┌──────────────────────────────────────────────┐")
            print(f"│              ABOUT ASTRA TECH                  │")
            print(f"├──────────────────────────────────────────────┤")
            print(f"│  ASTRA-SECURE CCTV Intelligence Suite v{VERSION}")
            print(f"│  Developed by {AUTHOR}")
            print(f"│  {BRAND} - 2026")
            print(f"│                                               │")
            print(f"│  {Fore.YELLOW}Purpose: Network Security Auditing")
            print(f"│  For educational & authorized testing only    │")
            print(f"│  Unauthorized use is a federal crime          │")
            print(f"│                                               │")
            print(f"│  {Fore.GREEN}Visit: https://astra-tech.security")
            print(f"└──────────────────────────────────────────────┘")
            input(f"\n{Fore.CYAN}Press Enter to continue...{Fore.RESET}")
        
        elif choice == "6":
            print(f"\n{Fore.RED}✗ Exiting ASTRA-SECURE Suite...{Fore.RESET}")
            print(f"{Fore.GREEN}Remember: Secure. Learn. Protect.{Fore.RESET}")
            sys.exit(0)
        
        else:
            print(f"{Fore.RED}✗ Invalid option{Fore.RESET}")
            time.sleep(1.5)

# ============== MAIN EXECUTION ==============

if __name__ == "__main__":
    try:
        # Check dependencies
        check_dependencies()
        # Run main menu
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}⚠️  Scan interrupted by user{Fore.RESET}")
        print(f"{Fore.GREEN}Remember: Secure. Learn. Protect.{Fore.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}✗ Error: {e}{Fore.RESET}")
        sys.exit(1)
