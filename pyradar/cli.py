import sys
from pyradar.network import parse_network
from pyradar.scanner import scan_network


def print_app_name() -> None:
    banner = r"""
  ____       ____           _
 |  _ \ _   |  _ \ __ _  __| | __ _ _ __
 | |_) | | | | |_) / _` |/ _` |/ _` | '__|
 |  __/| |_| |  _ < (_| | (_| | (_| | |
 |_|    \__, |_| \_\__,_|\__,_|\__,_|_|
          |___/

  Python Network Radar  |  For educational use only
    """
    print(banner)


def show_help() -> None:
    print(
        "\nUsage:\n"
        "  python -m pyradar [network]\n\n"
        "Options:\n"
        "  -h, --help    Show this help message and exit\n\n"
        "Network formats accepted:\n"
        "  (none)                  Auto-detect local network\n"
        "  192.168.1.0/24          Standard CIDR notation\n"
        "  192.168.1               Shorthand -> 192.168.1.0/24\n"
        "  192.168.1.5             Full IP   -> 192.168.1.0/24\n\n"
        "Examples:\n"
        "  python -m pyradar\n"
        "  python -m pyradar 192.168.1.0/24\n"
    )


def main() -> None:
    print_app_name()
    args = sys.argv[1:]

    if not args:
        try:
            network = parse_network()
        except Exception as exc:
            print(f"[!] Error auto-detecting network: {exc}")
            show_help()
            return

    elif args[0] in ("-h", "--help"):
        show_help()
        return

    elif len(args) == 1:
        try:
            network = parse_network(args[0])
        except ValueError as exc:
            print(f"[!] {exc}")
            show_help()
            return

    else:
        print("[!] Too many arguments.")
        show_help()
        return

    try:
        online_hosts = scan_network(network)
    except KeyboardInterrupt:
        print("\n[!] Scan aborted by user.")
        return

    print("\n" + "=" * 50)
    print(f"Scan complete. {len(online_hosts)} host(s) online:")
    print("=" * 50)
    for host in online_hosts:
        print(f"  {host}")
    print("=" * 50 + "\n")