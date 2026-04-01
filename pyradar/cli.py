import sys
from pyradar.network import parse_network
from pyradar.scanner import scan_network
from pyradar.ui import console, print_banner, print_help, print_results


def main() -> None:
    print_banner()
    args = sys.argv[1:]

    if not args:
        try:
            network = parse_network()
        except Exception as exc:
            console.print(f"[red][!] Error auto-detecting network: {exc}[/red]")
            print_help()
            return

    elif args[0] in ("-h", "--help"):
        print_help()
        return

    elif len(args) == 1:
        try:
            network = parse_network(args[0])
        except ValueError as exc:
            console.print(f"[red][!] {exc}[/red]")
            print_help()
            return

    else:
        console.print("[red][!] Too many arguments.[/red]")
        print_help()
        return

    try:
        online_hosts = scan_network(network)
    except KeyboardInterrupt:
        console.print("\n[yellow][!] Scan aborted by user.[/yellow]")
        return

    print_results(online_hosts)