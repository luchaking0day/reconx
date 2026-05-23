#!/usr/bin/env python3
import socket
import concurrent.futures
from modules.utils import print_section, print_found, print_open_port, print_info, print_warning, print_success, Colors


# Top 100 most common ports
TOP_100_PORTS = [
    21, 22, 23, 25, 53, 80, 81, 88, 110, 111,
    119, 123, 135, 137, 138, 139, 143, 161, 179, 194,
    389, 443, 445, 465, 500, 512, 513, 514, 587, 631,
    636, 993, 995, 1080, 1194, 1433, 1434, 1521, 1723, 2049,
    2083, 2096, 2181, 2375, 2376, 3000, 3306, 3389, 3690, 4443,
    4444, 4567, 4848, 5000, 5432, 5900, 5984, 6000, 6379, 6443,
    6881, 7001, 7070, 7443, 7474, 8000, 8008, 8080, 8081, 8443,
    8888, 8983, 9000, 9042, 9090, 9200, 9300, 9418, 9443, 9999,
    10000, 11211, 15672, 16379, 27017, 27018, 28017, 50000, 50070, 61616,
    80, 443, 8080, 8443, 3000, 5000, 4000, 9000, 7000, 6000,
]
TOP_100_PORTS = sorted(set(TOP_100_PORTS))


COMMON_SERVICES = {
    21: "FTP",        22: "SSH",         23: "Telnet",     25: "SMTP",
    53: "DNS",        80: "HTTP",        88: "Kerberos",   110: "POP3",
    111: "RPC",       119: "NNTP",       123: "NTP",       135: "RPC",
    137: "NetBIOS",   139: "NetBIOS",    143: "IMAP",      161: "SNMP",
    179: "BGP",       389: "LDAP",       443: "HTTPS",     445: "SMB",
    465: "SMTPS",     500: "IKE",        512: "rexec",     513: "rlogin",
    514: "syslog",    587: "SMTP",       631: "IPP",       636: "LDAPS",
    993: "IMAPS",     995: "POP3S",      1080: "SOCKS",    1194: "OpenVPN",
    1433: "MSSQL",    1521: "Oracle",    1723: "PPTP",     2049: "NFS",
    2181: "Zookeeper",2375: "Docker",    2376: "Docker",   3000: "Dev",
    3306: "MySQL",    3389: "RDP",       3690: "SVN",      4443: "HTTPS-alt",
    4444: "Metasploit",5000: "Flask",    5432: "PostgreSQL",5900: "VNC",
    5984: "CouchDB",  6379: "Redis",     7001: "WebLogic", 8000: "HTTP-alt",
    8008: "HTTP-alt", 8080: "HTTP-proxy",8081: "HTTP-alt", 8443: "HTTPS-alt",
    8888: "Jupyter",  9000: "PHP-FPM",   9090: "Prometheus",9200: "Elasticsearch",
    9418: "Git",      10000: "Webmin",   11211: "Memcached",27017: "MongoDB",
    50000: "DB2",     61616: "ActiveMQ",
}


def _grab_banner(ip: str, port: int, timeout: float) -> str:
    try:
        with socket.create_connection((ip, port), timeout=timeout) as s:
            s.settimeout(timeout)
            try:
                banner = s.recv(256).decode("utf-8", errors="ignore").strip()
                return banner[:60] if banner else ""
            except Exception:
                return ""
    except Exception:
        return ""


def _scan_port(ip: str, port: int, timeout: float) -> tuple[int, bool, str]:
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return port, True, ""
    except (socket.timeout, ConnectionRefusedError, OSError):
        return port, False, ""


def port_scan(target: str, top_n: int = 100, timeout: float = 1.0) -> dict:
    print_section("Port Scan")

    try:
        ip = socket.gethostbyname(target)
    except socket.gaierror:
        from modules.utils import print_error
        print_error(f"Cannot resolve {target}")
        return {"error": "dns resolution failed"}

    print_info(f"Resolved: {target} → {ip}")
    ports = TOP_100_PORTS[:top_n]
    print_info(f"Scanning {len(ports)} ports  |  Timeout: {timeout}s")
    print(f"    {'PORT':<8} {'STATE':<8} {'SERVICE':<16} BANNER")
    print(f"    {'─'*7} {'─'*7} {'─'*15} {'─'*20}")

    open_ports = {}

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(_scan_port, ip, p, timeout): p for p in ports}
        for future in concurrent.futures.as_completed(futures):
            port, is_open, _ = future.result()
            if is_open:
                service = COMMON_SERVICES.get(port, "unknown")
                banner = _grab_banner(ip, port, timeout)
                print_open_port(port, service, banner)
                open_ports[port] = {"service": service, "banner": banner}

    print()
    print_success(f"Found {len(open_ports)} open port(s).")
    return {"target_ip": ip, "open_ports": open_ports}
