#!/usr/bin/env python3


class Colors:
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    RESET   = "\033[0m"


def print_section(title: str):
    width = 60
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'─' * width}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}  ◈  {title.upper()}{Colors.RESET}")
    print(f"{Colors.CYAN}{'─' * width}{Colors.RESET}")


def print_success(msg: str):
    print(f"{Colors.GREEN}[+]{Colors.RESET} {msg}")


def print_info(msg: str):
    print(f"{Colors.BLUE}[*]{Colors.RESET} {msg}")


def print_warning(msg: str):
    print(f"{Colors.YELLOW}[!]{Colors.RESET} {msg}")


def print_error(msg: str):
    print(f"{Colors.RED}[-]{Colors.RESET} {msg}")


def print_found(key: str, value: str):
    print(f"    {Colors.DIM}{key:<20}{Colors.RESET} {Colors.WHITE}{value}{Colors.RESET}")


def print_open_port(port: int, service: str, banner: str = ""):
    line = f"    {Colors.GREEN}OPEN{Colors.RESET}  {Colors.BOLD}{port:<6}{Colors.RESET}  {Colors.CYAN}{service:<16}{Colors.RESET}"
    if banner:
        line += f"  {Colors.DIM}{banner[:50]}{Colors.RESET}"
    print(line)
