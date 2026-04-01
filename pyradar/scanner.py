import subprocess
import platform
import re
import concurrent.futures


def ping(ip: str):
    ip = str(ip)
    system = platform.system().lower()

    if system == "windows":
        cmd = ["ping", "-n", "1", "-w", "1000", ip]
    else:
        cmd = ["ping", "-c", "1", "-W", "1", ip]

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=2,
        )
        if re.search(r"ttl", result.stdout, re.IGNORECASE):
            return ip
    except subprocess.TimeoutExpired:
        return None
    except Exception:
        return None

    return None


def scan_network(network, max_workers: int = 100) -> list:
    print(f"\n[*] Scanning network: {network}")
    print(f"[*] Total hosts to probe: {network.num_addresses - 2}\n")

    online = []

    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(ping, str(ip)): str(ip)
                for ip in network.hosts()
            }
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    if result:
                        online.append(result)
                        print(f"  [+] Host online: {result}")
                except Exception:
                    continue

    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user. Returning partial results...")

    return sorted(online, key=lambda x: tuple(map(int, x.split("."))))