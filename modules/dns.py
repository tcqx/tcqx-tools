import socket

from core import ui, animations, config


def _resolve_ipv4(domain):
    try:
        return socket.gethostbyname(domain)
    except Exception:
        return None


def _resolve_all(domain):
    """Retourne toutes les adresses IPv4/IPv6 disponibles pour le domaine."""
    ipv4_list = set()
    ipv6_list = set()
    try:
        results = socket.getaddrinfo(domain, None)
        for family, _, _, _, sockaddr in results:
            if family == socket.AF_INET:
                ipv4_list.add(sockaddr[0])
            elif family == socket.AF_INET6:
                ipv6_list.add(sockaddr[0])
    except Exception:
        pass
    return sorted(ipv4_list), sorted(ipv6_list)


def _reverse_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return None


def run(console):
    ui.print_module_header(console, "DNS // Resolution de domaine")

    domain = ui.prompt(console, "Entrez un nom de domaine (ex: example.com) > ")
    domain = domain.strip()

    if not domain:
        animations.print_error(console, "Aucun domaine fourni.")
        ui.press_enter(console)
        return

    animations.loading_bar(console, f"Resolution de {domain}", duration=0.6)

    ipv4_list, ipv6_list = _resolve_all(domain)
    primary_ip = ipv4_list[0] if ipv4_list else _resolve_ipv4(domain)
    reverse_host = _reverse_hostname(primary_ip) if primary_ip else None

    console.print()

    if not ipv4_list and not ipv6_list:
        animations.print_error(console, f"Impossible de resoudre '{domain}'.")
        ui.press_enter(console)
        return

    rows = {
        "Domaine": domain,
        "IPv4": ", ".join(ipv4_list) if ipv4_list else "Non disponible",
        "IPv6": ", ".join(ipv6_list) if ipv6_list else "Non disponible",
        "Hostname (reverse DNS)": reverse_host,
    }

    ui.info_panel(console, "RESULTAT DNS", rows)

    console.print()
    animations.print_ok(console, "Resolution terminee.")
    ui.press_enter(console)
