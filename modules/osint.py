import socket

from core import ui, animations, config

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


PLATFORMS = {
    "GitHub": "https://github.com/{username}",
    "Twitter / X": "https://x.com/{username}",
    "Instagram": "https://www.instagram.com/{username}/",
    "Reddit": "https://www.reddit.com/user/{username}/",
    "Twitch": "https://www.twitch.tv/{username}",
}

SEARCH_ENGINES = {
    "Google": "https://www.google.com/search?q={query}",
    "Bing": "https://www.bing.com/search?q={query}",
    "DuckDuckGo": "https://duckduckgo.com/?q={query}",
}


def _menu(console):
    ui.print_module_header(console, "OSINT // Outils publics")
    console.print(f" [{config.COLOR_ACCENT}][1][/] Informations sur un domaine")
    console.print(f" [{config.COLOR_ACCENT}][2][/] Generer des liens de recherche")
    console.print(f" [{config.COLOR_ACCENT}][3][/] Verifier un pseudo sur des plateformes publiques")
    console.print(f" [{config.COLOR_ACCENT}][0][/] Retour")
    console.print()
    return ui.prompt(console, "Choix > ")


def _domain_info(console):
    domain = ui.prompt(console, "Domaine a analyser (ex: example.com) > ").strip()
    if not domain:
        animations.print_error(console, "Aucun domaine fourni.")
        ui.press_enter(console)
        return

    animations.loading_bar(console, f"Recherche d'informations sur {domain}", duration=0.5)

    try:
        ip = socket.gethostbyname(domain)
    except Exception:
        ip = None

    rows = {
        "Domaine": domain,
        "IP resolue": ip or "Non resolue",
        "Fiche WHOIS publique": f"https://who.is/whois/{domain}",
        "Fiche DNS publique": f"https://dnschecker.org/#A/{domain}",
    }
    console.print()
    ui.info_panel(console, "DOMAINE", rows)
    console.print()
    animations.print_ok(console, "Recherche terminee.")
    ui.press_enter(console)


def _generate_search_links(console):
    query = ui.prompt(console, "Terme a rechercher > ").strip()
    if not query:
        animations.print_error(console, "Aucun terme fourni.")
        ui.press_enter(console)
        return

    encoded = query.replace(" ", "+")
    rows = {name: url.format(query=encoded) for name, url in SEARCH_ENGINES.items()}

    console.print()
    ui.info_panel(console, f"LIENS DE RECHERCHE // '{query}'", rows)
    console.print()
    animations.print_ok(console, "Liens generes.")
    ui.press_enter(console)


def _check_username(console):
    username = ui.prompt(console, "Pseudo a verifier > ").strip()
    if not username:
        animations.print_error(console, "Aucun pseudo fourni.")
        ui.press_enter(console)
        return

    if not REQUESTS_AVAILABLE:
        animations.print_error(
            console, "Le module 'requests' n'est pas installe (pip install requests)."
        )
        ui.press_enter(console)
        return

    console.print()
    results = {}

    for platform_name, url_template in PLATFORMS.items():
        url = url_template.format(username=username)
        animations.spinner(console, f"Verification sur {platform_name}...", duration=0.4)
        try:
            response = requests.get(
                url,
                timeout=4,
                headers={"User-Agent": "Mozilla/5.0 (TCQX-Terminal OSINT tool)"},
            )
            if response.status_code == 200:
                results[platform_name] = "[bright_yellow]Probablement pris[/bright_yellow]"
            elif response.status_code == 404:
                results[platform_name] = "[bright_green]Probablement disponible[/bright_green]"
            else:
                results[platform_name] = f"Statut HTTP {response.status_code}"
        except Exception:
            results[platform_name] = "Verification impossible (reseau)"

    ui.info_panel(console, f"DISPONIBILITE DU PSEUDO '{username}'", results)
    console.print()
    console.print(
        f"[{config.COLOR_DIM}]Note : ce resultat se base uniquement sur le code HTTP "
        f"de la page de profil publique et peut ne pas etre fiable a 100%.[/]"
    )
    console.print()
    animations.print_ok(console, "Verification terminee.")
    ui.press_enter(console)


def run(console):
    while True:
        choice = _menu(console)
        if choice == "1":
            _domain_info(console)
        elif choice == "2":
            _generate_search_links(console)
        elif choice == "3":
            _check_username(console)
        elif choice == "0" or choice == "":
            return
        else:
            animations.print_error(console, "Choix invalide.")
            ui.press_enter(console)
