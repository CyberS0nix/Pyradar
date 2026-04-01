# 🛰️ PyRadar

> A professional Python network scanner for cybersecurity education — detects online hosts, resolves hostnames, fingerprints operating systems, scans open ports, and exports results.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Version](https://img.shields.io/badge/Version-2.0.0-red?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey?style=flat-square)

---

## ⚠️ Disclaimer

This tool is for **educational purposes only**.
Only scan networks and devices that **you own or have explicit permission to test**.
Unauthorized network scanning may violate local laws and regulations.
The author assumes **no responsibility** for misuse of this tool.

---

## ✨ Features

- 🔍 **Host Discovery** — Detects all online devices on a network using ICMP ping
- 🌐 **DNS Resolution** — Resolves IP addresses to hostnames automatically
- 🖥️ **OS Fingerprinting** — Guesses the operating system via TTL analysis
- 🔌 **Port Scanning** — TCP connect scan on 17 common ports with service names
- 🧭 **MAC Address Detection** — Retrieves MAC addresses from the ARP table
- 📊 **Rich Terminal UI** — Colored output, live progress bar, and formatted tables
- 💾 **Export Results** — Save scan results as JSON or CSV for reporting
- ⚡ **Multi-threaded** — Fast parallel scanning with up to 100 concurrent threads

---

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip

### Clone the repository

```bash
git clone https://github.com/taguianas/Pyradar.git
cd Pyradar
```

### Install dependencies

```bash
pip install -r requirements.txt
```

Or install as a package (enables the `pyradar` command globally):

```bash
pip install .
```

---

## 🚀 Usage

### Basic scan (auto-detects your local network)

```bash
python -m pyradar
```

### Scan a specific network

```bash
python -m pyradar 192.168.1.0/24
```

### Shorthand formats

```bash
python -m pyradar 192.168.1        # treated as 192.168.1.0/24
python -m pyradar 192.168.1.5      # treated as 192.168.1.0/24
```

### Export results

```bash
python -m pyradar --output json    # saves pyradar_YYYYMMDD_HHMMSS.json
python -m pyradar --output csv     # saves pyradar_YYYYMMDD_HHMMSS.csv
```

### Show help

```bash
python -m pyradar --help
```

---

## 📋 Example Output

```
Scanning 192.168.1.0/24 — 254 hosts

  ● 192.168.1.1 is online
  ● 192.168.1.10 is online

Enriching host data...

          Scan Results — 2 host(s) online
┌────┬───────────────┬──────────────┬───────────────────┬──────────────┬──────────────────────────────┬──────────┐
│ #  │ IP Address    │ Hostname     │ MAC               │ OS Guess     │ Open Ports                   │ Status   │
├────┼───────────────┼──────────────┼───────────────────┼──────────────┼──────────────────────────────┼──────────┤
│ 1  │ 192.168.1.1   │ router.local │ N/A               │ Linux/macOS  │ 80 (HTTP), 443 (HTTPS)       │ ● Online │
│ 2  │ 192.168.1.10  │ Anas         │ N/A               │ Windows      │ 135 (RPC), 445 (SMB)         │ ● Online │
└────┴───────────────┴──────────────┴───────────────────┴──────────────┴──────────────────────────────┴──────────┘
```

---

## 🗂️ Project Structure

```
Pyradar/
├── pyradar/
│   ├── __init__.py       # Version info
│   ├── __main__.py       # Entry point (python -m pyradar)
│   ├── cli.py            # Argument parsing and main flow
│   ├── network.py        # IP/mask detection and network parsing
│   ├── scanner.py        # Ping scanning and thread management
│   ├── resolver.py       # DNS, MAC, OS fingerprinting, port scanning
│   ├── exporter.py       # JSON and CSV export
│   └── ui.py             # Rich terminal UI components
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

## 🔌 Scanned Ports

| Port | Service   | Port | Service   |
|------|-----------|------|-----------|
| 21   | FTP       | 443  | HTTPS     |
| 22   | SSH       | 445  | SMB       |
| 23   | Telnet    | 3306 | MySQL     |
| 25   | SMTP      | 3389 | RDP       |
| 53   | DNS       | 5900 | VNC       |
| 80   | HTTP      | 8080 | HTTP-Alt  |
| 110  | POP3      | 8443 | HTTPS-Alt |
| 135  | RPC       |      |           |
| 139  | NetBIOS   |      |           |

---

## 🛠️ Dependencies

| Package | Purpose |
|---------|---------|
| `rich`  | Terminal UI, colors, tables, progress bar |
| `scapy` | Network packet manipulation (ARP) |

---

## 👥 Authors

- **Xen0w** 
- **taguianas**

---

## 📄 License

This project is licensed under the MIT License.
See the [LICENSE](LICENSE) file for details.