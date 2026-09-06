import webbrowser

from core import ui, animations, config


def run(console):
    ui.print_module_header(console, "Discord // Liens officiels")

    rows = {
        "GitHub": config.GITHUB_URL,
        "Guns.lol": config.GUNSLOL_URL,
        "Discord": config.DISCORD_INVITE,
    }

    ui.info_panel(console, "LIENS", rows)
    console.print()

    choice = ui.prompt(
        console,
        "Ouvrir un lien dans le navigateur ? (github/guns/discord/non) > ",
        default="non",
    ).lower().strip()

    targets = {
        "github": config.GITHUB_URL,
        "guns": config.GUNSLOL_URL,
        "discord": config.DISCORD_INVITE,
    }

    if choice in targets:
        try:
            webbrowser.open(targets[choice])
            animations.print_ok(console, f"Ouverture de {targets[choice]}")
        except Exception:
            animations.print_error(console, "Impossible d'ouvrir le navigateur.")
    else:
        animations.print_ok(console, "Aucun lien ouvert.")

    ui.press_enter(console)
