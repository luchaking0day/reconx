#!/usr/bin/env python3
import socket
import subprocess
from modules.utils import print_section, print_found, print_warning, print_error, Colors


RECORD_TYPES = ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA", "CAA"]


def _dig(domain: str, record: str) -> list[str]:
    """Run dig and return parsed answer lines."""
    try:
        proc = subprocess.run(
            ["dig", "+noall", "+answer", "+nocmd", record, domain],
            capture_output=True, text=True, timeout=10
        )
        lines = [l.strip() for l in proc.stdout.strip().splitlines() if l.strip()]
        return lines
    except FileNotFoundError:
        return []
    except subprocess.TimeoutExpired:
        return []


def _resolve_fallback(domain: str) -> list[str]:
    """Simple A record fallback using socket."""
    try:
        infos = socket.getaddrinfo(domain, None)
        return list({i[4][0] for i in infos})
    except socket.gaierror:
        return []


def dns_enum(target: str) -> dict:
    print_section("DNS Enumeration")
    results = {}

    has_dig = subprocess.run(["which", "dig"], capture_output=True).returncode == 0

    if not has_dig:
        print_warning("'dig' not found. Falling back to socket (A records only).")
        ips = _resolve_fallback(target)
        if ips:
            results["A"] = ips
            for ip in ips:
                print_found("A", ip)

                # Reverse DNS
                try:
                    hostname = socket.gethostbyaddr(ip)[0]
                    print_found("PTR", hostname)
                    results.setdefault("PTR", []).append(hostname)
                except Exception:
                    pass
        return results

    for rtype in RECORD_TYPES:
        lines = _dig(target, rtype)
        if not lines:
            continue

        records = []
        for line in lines:
            parts = line.split()
            if len(parts) >= 5:
                value = " ".join(parts[4:])
            elif len(parts) >= 1:
                value = parts[-1]
            else:
                continue
            records.append(value)
            print_found(rtype, value)

        if records:
            results[rtype] = records

    if not results:
        print_warning("No DNS records found.")

    # Reverse PTR for each A record
    for ip in results.get("A", []):
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            print_found("PTR", f"{ip} → {hostname}")
            results.setdefault("PTR", []).append(f"{ip} → {hostname}")
        except Exception:
            pass

    return results
