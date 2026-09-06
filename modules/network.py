import socket
import re

from core import ui, animations, config
from core.utils import safe_run, get_hostname, get_local_ip, platform_name


def _get_gateway():
    """Recupere la passerelle par defaut (Windows / Linux / macOS)."""
    if config.IS_WINDOWS:
        output = safe_run("ipconfig")
        if output:
            match = re.search(r"Passerelle par d.faut.*?:\s*([\d.]+)", output)
            if not match:
                match = re.search(r"Default Gateway.*?:\s*([\d.]+)", output)
            if match:
                return match.group(1)
        return None

    output = safe_run("ip route show default")
    if output:
        match = re.search(r"default via ([\d.]+)", output)
        if match:
            return match.group(1)
    return None


def _get_dns_servers():
    """Recupere les serveurs DNS configures sur la machine."""
    if config.IS_WINDOWS:
        output = safe_run("ipconfig /all")
        if output:
            servers = re.findall(r"Serveurs DNS.*?:\s*([\d.]+)", output)
            if not servers:
                servers = re.findall(r"DNS Servers.*?:\s*([\d.]+)", output)
            if servers:
                return ", ".join(dict.fromkeys(servers))
        return None

    output = safe_run("cat /etc/resolv.conf")
    if output:
        servers = re.findall(r"nameserver\s+([\d.]+)", output)
        if servers:
            return ", ".join(servers)
    return None


def _get_wifi_info():
    """Recupere le SSID et la puissance du signal Wi-Fi (Windows uniquement)."""
    if not config.IS_WINDOWS:
        return None

    output = safe_run("netsh wlan show interfaces")
    if not output:
        return None

    info = {}
    ssid_match = re.search(r"^\s*SSID\s*:\s*(.+)$", output, re.MULTILINE)
    signal_match = re.search(r"Signal\s*:\s*(.+)", output)
    state_match = re.search(r"State\s*:\s*(.+)", output)

    if ssid_match:
        info["SSID"] = ssid_match.group(1).strip()
    if signal_match:
        info["Signal"] = signal_match.group(1).strip()
    if state_match:
        info["Etat"] = state_match.group(1).strip()

    return info or None


def _get_interfaces_summary():
    """Retourne un resume texte des interfaces reseau detectees."""
    try:
        hostname = socket.gethostname()
        addr_info = socket.getaddrinfo(hostname, None)
        ips = sorted({item[4][0] for item in addr_info})
        return ", ".join(ips) if ips else None
    except Exception:
        return None


def run(console):
    ui.print_module_header(console, "Network // Informations reseau")
    animations.loading_bar(console, "Analyse des interfaces reseau", duration=0.5)

    rows = {
        "Hostname": get_hostname(),
        "Plateforme": platform_name(),
        "IP locale": get_local_ip(),
        "Adresses detectees": _get_interfaces_summary(),
        "Passerelle (gateway)": _get_gateway(),
        "Serveurs DNS": _get_dns_servers(),
    }

    ui.info_panel(console, "RESEAU LOCAL", rows)

    wifi = _get_wifi_info()
    console.print()
    if wifi:
        ui.info_panel(console, "WI-FI", wifi)
    else:
        console.print(
            f"[{config.COLOR_DIM}]Aucune information Wi-Fi disponible sur cette machine.[/]"
        )

    console.print()
    animations.print_ok(console, "Analyse reseau terminee.")
    ui.press_enter(console)
