#!/usr/bin/env python3
from modules.utils import Colors


BANNER = r"""
 ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗██╗  ██╗
 ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║╚██╗██╔╝
 ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║ ╚███╔╝
 ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║ ██╔██╗
 ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║██╔╝ ██╗
 ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝
"""

SUBTITLE = "   Domain & IP OSINT Reconnaissance Tool  v1.0"
META     = "   by YourName | github.com/yourusername/reconx"


def print_banner():
    print(f"{Colors.CYAN}{Colors.BOLD}{BANNER}{Colors.RESET}", end="")
    print(f"{Colors.WHITE}{SUBTITLE}{Colors.RESET}")
    print(f"{Colors.DIM}{META}{Colors.RESET}")
    print(f"{Colors.CYAN}{'─' * 55}{Colors.RESET}\n")
