import socket
import ipaddress
import platform
import subprocess
import re


def get_local_ip_and_mask() -> tuple:
    system = platform.system().lower()

    if system == "windows":
        output = subprocess.check_output("ipconfig", universal_newlines=True)
        ip_match   = re.search(r"IPv4 Address[. ]*: ([\d.]+)", output)
        mask_match = re.search(r"Subnet Mask[. ]*: ([\d.]+)", output)
        if ip_match and mask_match:
            return ip_match.group(1), mask_match.group(1)
    else:
        try:
            output = subprocess.check_output(
                "ifconfig", shell=True, universal_newlines=True
            )
            ip_match = re.search(
                r"inet ([\d.]+).*?netmask (0x[\da-f]+|[\d.]+)", output
            )
            if ip_match:
                ip   = ip_match.group(1)
                mask = ip_match.group(2)
                if mask.startswith("0x"):
                    mask = socket.inet_ntoa(int(mask, 16).to_bytes(4, "big"))
                return ip, mask
        except Exception:
            pass

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()

    return ip, "255.255.255.0"


def mask_to_cidr(mask: str) -> int:
    return sum(bin(int(octet)).count("1") for octet in mask.split("."))


def parse_network(arg=None):
    if not arg:
        ip, mask = get_local_ip_and_mask()
        cidr = mask_to_cidr(mask)
        return ipaddress.ip_network(f"{ip}/{cidr}", strict=False)

    if "/" in arg:
        return ipaddress.ip_network(arg, strict=False)

    if re.match(r"^\d+\.\d+\.\d+$", arg):
        return ipaddress.ip_network(arg + ".0/24", strict=False)

    if re.match(r"^\d+\.\d+\.\d+\.\d+$", arg):
        return ipaddress.ip_network(arg + "/24", strict=False)

    raise ValueError(f"Unrecognised network format: '{arg}'")