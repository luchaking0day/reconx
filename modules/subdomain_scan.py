#!/usr/bin/env python3
import socket
import concurrent.futures
import os
from modules.utils import print_section, print_found, print_warning, print_success, print_info, Colors


def _resolve(subdomain: str) -> tuple[str, list[str]] | None:
    try:
        infos = socket.getaddrinfo(subdomain, None, socket.AF_UNSPEC, socket.SOCK_STREAM)
        ips = list({i[4][0] for i in infos})
        return subdomain, ips
    except (socket.gaierror, OSError):
        return None


def _load_wordlist(path: str) -> list[str]:
    if not os.path.isfile(path):
        print_warning(f"Wordlist not found: {path}")
        return []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


def subdomain_scan(target: str, wordlist_path: str, timeout: float = 1.0, threads: int = 50) -> dict:
    print_section("Subdomain Brute-Force")

    words = _load_wordlist(wordlist_path)
    if not words:
        return {"error": "no wordlist"}

    socket.setdefaulttimeout(timeout)
    print_info(f"Wordlist: {len(words)} entries  |  Threads: {threads}")

    found = {}
    candidates = [f"{w}.{target}" for w in words]

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(_resolve, c): c for c in candidates}
        done = 0
        for future in concurrent.futures.as_completed(futures):
            done += 1
            result = future.result()
            if result:
                subdomain, ips = result
                found[subdomain] = ips
                print_found(subdomain, ", ".join(ips))
            # Progress bar
            if done % 50 == 0 or done == len(candidates):
                pct = int(done / len(candidates) * 30)
                bar = f"[{'█' * pct}{'░' * (30 - pct)}] {done}/{len(candidates)}"
                print(f"\r    {Colors.DIM}{bar}{Colors.RESET}", end="", flush=True)

    print()  # newline after progress
    print_success(f"Found {len(found)} subdomains.")
    return found
