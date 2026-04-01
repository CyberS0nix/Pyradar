import subprocess
import platform
import re
import concurrent.futures
from pyradar.ui import console, make_progress


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
    hosts = list(network.hosts())
    total = len(hosts)
    online = []

    console.print(f"\n[bold]Scanning[/bold] [cyan]{network}[/cyan] — [dim]{total} hosts[/dim]\n")

    try:
        with make_progress(total) as progress:
            task = progress.add_task("Scanning...", total=total)
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {executor.submit(ping, str(ip)): str(ip) for ip in hosts}
                for future in concurrent.futures.as_completed(futures):
                    progress.advance(task)
                    try:
                        result = future.result()
                        if result:
                            online.append(result)
                            console.print(f"  [green]●[/green] [cyan]{result}[/cyan] is online")
                    except Exception:
                        continue

    except KeyboardInterrupt:
        console.print("\n[yellow][!] Scan interrupted by user.[/yellow]")

    return sorted(online, key=lambda x: tuple(map(int, x.split("."))))