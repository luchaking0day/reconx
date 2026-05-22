#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ReconX - Domain & IP OSINT Reconnaissance Tool
Author: luchaking0day
GitHub: https://github.com/luchaking0day/reconx
"""

import argparse
import sys
import os
import json
from datetime import datetime

from modules.banner import print_banner
from modules.whois_lookup import whois_lookup
from modules.dns_enum import dns_enum
from modules.subdomain_scan import subdomain_scan
from modules.port_scan import port_scan
from modules.utils import print_section, print_success, print_info, print_error, Colors


def parse_args():
    parser = argparse.ArgumentParser(
        prog="reconx",
        description="ReconX - Domain & IP OSINT Reconnaissance Tool",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("target", help="Target domain or IP address (e.g. example.com)")
    parser.add_argument("-w", "--whois",   action="store_true", help="Run WHOIS lookup")
    parser.add_argument("-d", "--dns",     action="store_true", help="Run DNS enumeration")
    parser.add_argument("-s", "--subdomains", action="store_true", help="Run subdomain brute-force")
    parser.add_argument("-p", "--ports",   action="store_true", help="Run port scan")
    parser.add_argument("-a", "--all",     action="store_true", help="Run all modules")
    parser.add_argument("-o", "--output",  metavar="FILE",      help="Save results to file (JSON)")
    parser.add_argument("--wordlist",      metavar="FILE",      help="Custom wordlist for subdomain scan")
    parser.add_argument("--top-ports",     type=int, default=100, metavar="N",
                        help="Number of top ports to scan (default: 100)")
    parser.add_argument("--timeout",       type=float, default=1.0,
                        help="Timeout in seconds for connections (default: 1.0)")
    return parser


def main():
    print_banner()

    parser = parse_args()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()
    target = args.target.strip().lower().replace("https://", "").replace("http://", "").rstrip("/")

    run_all = args.all or not any([args.whois, args.dns, args.subdomains, args.ports])

    print_info(f"Target  : {Colors.BOLD}{target}{Colors.RESET}")
    print_info(f"Started : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print_info(f"Modules : {'ALL' if run_all else ', '.join(filter(None, [
        'WHOIS'      if (args.whois or run_all) else '',
        'DNS'        if (args.dns or run_all) else '',
        'SUBDOMAINS' if (args.subdomains or run_all) else '',
        'PORTS'      if (args.ports or run_all) else '',
    ]))}")

    results = {
        "target":    target,
        "timestamp": datetime.now().isoformat(),
        "modules":   {}
    }

    # ── WHOIS ──
    if args.whois or run_all:
        data = whois_lookup(target)
        results["modules"]["whois"] = data

    # ── DNS ──
    if args.dns or run_all:
        data = dns_enum(target)
        results["modules"]["dns"] = data

    # ── Subdomains ──
    if args.subdomains or run_all:
        wordlist = args.wordlist or os.path.join(os.path.dirname(__file__), "wordlists", "subdomains.txt")
        data = subdomain_scan(target, wordlist, args.timeout)
        results["modules"]["subdomains"] = data

    # ── Ports ──
    if args.ports or run_all:
        data = port_scan(target, args.top_ports, args.timeout)
        results["modules"]["ports"] = data

    # ── Save output ──
    if args.output:
        out_path = args.output if args.output.endswith(".json") else args.output + ".json"
        os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
        with open(out_path, "w") as f:
            json.dump(results, f, indent=2, default=str)
        print_success(f"\nResults saved → {out_path}")

    print(f"\n{Colors.DIM}{'─' * 60}{Colors.RESET}")
    print_success("Scan complete.")


if __name__ == "__main__":
    main()
