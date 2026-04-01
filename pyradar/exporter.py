import json
import csv
from datetime import datetime


def _filename(ext: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"pyradar_{timestamp}.{ext}"


def export_json(hosts: list) -> str:
    filename = _filename("json")
    with open(filename, "w") as f:
        json.dump(hosts, f, indent=4)
    return filename


def export_csv(hosts: list) -> str:
    filename = _filename("csv")
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["IP", "Hostname", "MAC", "OS", "Open Ports"])
        for host in hosts:
            ports = ", ".join(f"{p} ({s})" for p, s in host["ports"])
            writer.writerow([
                host["ip"],
                host["hostname"],
                host["mac"],
                host["os"],
                ports,
            ])
    return filename
