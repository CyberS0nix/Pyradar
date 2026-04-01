import sys
from pyradar.network import parse_network
from pyradar.scanner import scan_network
from pyradar.ui import console, print_banner, print_help, print_results
from pyradar.exporter import export_json, export_csv


def main() -> None:
    print_banner()
    args = sys.argv[1:]

    # Parse --output flag
    output_format = None
    if "--output" in args:
        idx = args.index("--output")
        if idx + 1 < len(args):
            output_format = args[idx + 1].lower()
            args = [a for i, a in enumerate(args) if i != idx and i != idx + 1]
        else:
            console.print("[red][!] --output requires a format: json or csv[/red]")
            return

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

    # Export if requested
    if output_format == "json":
        filename = export_json(online_hosts)
        console.print(f"[green][+] Results saved to {filename}[/green]\n")
    elif output_format == "csv":
        filename = export_csv(online_hosts)
        console.print(f"[green][+] Results saved to {filename}[/green]\n")
    elif output_format:
        console.print("[red][!] Unknown format. Use 'json' or 'csv'[/red]\n")