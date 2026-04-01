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
  
