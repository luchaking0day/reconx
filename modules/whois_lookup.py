#!/usr/bin/env python3
import subprocess
import re
from modules.utils import print_section, print_found, print_warning, print_error, Colors


FIELDS = {
    "Domain Name":        r"Domain Name:\s*(.+)",
    "Registrar":          r"Registrar:\s*(.+)",
    "Registrant Org":     r"Registrant Organization:\s*(.+)",
    "Registrant Country": r"Registrant Country:\s*(.+)",
    "Registrant Email":   r"Registrant Email:\s*(.+)",
    "Created":            r"Creation Date:\s*(.+)",
    "Updated":            r"Updated Date:\s*(.+)",
    "Expires":            r"Expiry Date:\s*(.+)",
    "Name Servers":       r"Name Server:\s*(.+)",
    "Status":             r"Domain Status:\s*(.+)",
    "DNSSEC":             r"DNSSEC:\s*(.+)",
}


def whois_lookup(target: str) -> dict:
    print_section("WHOIS Lookup")
    result = {}

    try:
        proc = subprocess.run(
            ["whois", target],
            capture_output=True, text=True, timeout=15
        )
        raw = proc.stdout
    except FileNotFoundError:
        print_warning("'whois' not found. Install: sudo apt install whois")
        return {"error": "whois not installed"}
    except subprocess.TimeoutExpired:
        print_error("WHOIS query timed out.")
        return {"error": "timeout"}

    if not raw.strip():
        print_warning("No WHOIS data returned.")
        return {}

    seen_ns = set()
    seen_status = set()

    for label, pattern in FIELDS.items():
        matches = re.findall(pattern, raw, re.IGNORECASE)
        if not matches:
            continue

        if label == "Name Servers":
            unique = []
            for m in matches:
                ns = m.strip().lower()
                if ns not in seen_ns:
                    seen_ns.add(ns)
                    unique.append(ns)
            if unique:
                result[label] = unique
                for ns in unique:
                    print_found(label, ns)
                    label = ""
        elif label == "Status":
            unique = []
            for m in matches:
                status = m.strip().split()[0]
                if status not in seen_status:
                    seen_status.add(status)
                    unique.append(status)
            if unique:
                result[label] = unique
                for s in unique[:3]:
                    print_found(label, s)
                    label = ""
        else:
            value = matches[0].strip()
            result[label] = value
            print_found(label, value)

    if not result:
        print_warning("Could not parse WHOIS data (may be rate-limited or private).")

    return result
