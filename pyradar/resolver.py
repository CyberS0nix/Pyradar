import socket
import re
import subprocess
from typing import Optional


def resolve_hostname(ip: str) -> str:
    """Resolve IP to hostname via DNS."""
    try:
        return socket.getfqdn(ip)
    except Exception:
        return "N/A"


def guess_os(ip: str) -> str:
    """Guess OS based on TTL value from ping reply."""
    try:
        result = subprocess.run(
            ["ping", "-n", "1", "-w", "1000", ip],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=2,
        )
        match = re.search(r"TTL=(\d+)", result.stdout, re.IGNORECASE)
        if match:
            ttl = int(match.group(1))
            if ttl <= 64:
                return "Linux / macOS"
            elif ttl <= 128:
                return "Windows"
            else:
                return "Network Device"
    except Exception:
        pass
    return "Unknown"


def get_mac_address(ip: str) -> str:
    """Get MAC address from ARP table (Windows)."""
    try:
        result = subprocess.run(
            ["arp", "-a", ip],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=2,
        )
        match = re.search(
            r"([0-9a-f]{2}[-:]){5}[0-9a-f]{2}", result.stdout, re.IGNORECASE
        )
        if match:
            return match.group(0).upper()
    except Exception:
        pass
    return "N/A"


def enrich_host(ip: str) -> dict:
    """Run all enrichment functions for a single host."""
    return {
        "ip":       ip,
        "hostname": resolve_hostname(ip),
        "mac":      get_mac_address(ip),
        "os":       guess_os(ip),
    }
  

COMMON_PORTS = {
    21:   "FTP",
    22:   "SSH",
    23:   "Telnet",
    25:   "SMTP",
    53:   "DNS",
    80:   "HTTP",
    110:  "POP3",
    135:  "RPC",
    139:  "NetBIOS",
    143:  "IMAP",
    443:  "HTTPS",
    445:  "SMB",
    3306: "MySQL",
    3389: "RDP",
    5900: "VNC",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
}


def scan_ports(ip: str) -> list:
    """TCP connect scan on common ports."""
    open_ports = []
    for port in COMMON_PORTS:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            if s.connect_ex((ip, port)) == 0:
                open_ports.append((port, COMMON_PORTS[port]))
            s.close()
        except Exception:
            pass
    return open_ports


def enrich_host(ip: str) -> dict:
    """Run all enrichment functions for a single host."""
    ports = scan_ports(ip)
    return {
        "ip":       ip,
        "hostname": resolve_hostname(ip),
        "mac":      get_mac_address(ip),
        "os":       guess_os(ip),
        "ports":    ports,
    }
    
