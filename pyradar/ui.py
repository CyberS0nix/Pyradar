from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich import box

console = Console()


def print_banner() -> None:
    banner = r"""
  ____       ____           _
 |  _ \ _   |  _ \ __ _  __| | __ _ _ __
 | |_) | | | | |_) / _` |/ _` |/ _` | '__|
 |  __/| |_| |  _ < (_| | (_| | (_| | |
 |_|    \__, |_| \_\__,_|\__,_|\__,_|_|
          |___/
    """
    console.print(Panel(banner, subtitle="[dim]❚█══  CyberS0nix  ══█❚[/dim]", style="bold green"))


def print_help() -> None:
    console.print("\n[bold cyan]Usage:[/bold cyan]")
    console.print("  python -m pyradar [network]\n")
    console.print("[bold cyan]Options:[/bold cyan]")
    console.print("  -h, --help    Show this help message\n")
    console.print("[bold cyan]Network formats:[/bold cyan]")
    console.print("  [green](none)[/green]            Auto-detect local network")
    console.print("  [green]192.168.1.0/24[/green]   Standard CIDR")
    console.print("  [green]192.168.1[/green]        Shorthand -> 192.168.1.0/24")
    console.print("  [green]192.168.1.5[/green]      Full IP   -> 192.168.1.0/24\n")
    console.print("[bold cyan]Examples:[/bold cyan]")
    console.print("  python -m pyradar")
    console.print("  python -m pyradar 192.168.1.0/24\n")


def print_results(hosts: list) -> None:
    table = Table(
        title=f"Scan Results — {len(hosts)} host(s) online",
        box=box.ROUNDED,
        style="bold",
        header_style="bold magenta",
    )
    table.add_column("#",          style="dim",    width=4)
    table.add_column("IP Address", style="cyan",   width=16)
    table.add_column("Hostname",   style="white",  width=20)
    table.add_column("MAC",        style="yellow", width=20)
    table.add_column("OS Guess",   style="green",  width=14)
    table.add_column("Open Ports", style="red",    width=30)
    table.add_column("Status",     style="green",  width=10)

    for i, host in enumerate(hosts, 1):
        # Format ports as "80 (HTTP), 443 (HTTPS)"
        ports_str = ", ".join(
            f"{p} ({s})" for p, s in host["ports"]
        ) if host["ports"] else "None"

        table.add_row(
            str(i),
            host["ip"],
            host["hostname"],
            host["mac"],
            host["os"],
            ports_str,
            "● Online",
        )

    console.print()
    console.print(table)
    console.print()


def make_progress(total: int):
    return Progress(
        SpinnerColumn(),
        TextColumn("[bold green]{task.description}"),
        BarColumn(),
        TextColumn("[cyan]{task.completed}/{task.total} hosts"),
        console=console,
        transient=True,
    )