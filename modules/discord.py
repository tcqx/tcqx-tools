import webbrowser

from core import ui, config


def run(console):
    while True:
        ui.print_module_header(
            console,
            "Links // TCQX"
        )

        console.print(
            f" [{config.COLOR_ACCENT}][1][/] Discord"
        )

        console.print(
            f" [{config.COLOR_ACCENT}][2][/] GitHub"
        )

        console.print(
            f" [{config.COLOR_ACCENT}][3][/] Guns.lol"
        )

        console.print(
            f" [{config.COLOR_ACCENT}][0][/] Retour"
        )

        console.print()

        choice = ui.prompt(
            console,
            "Choix > "
        ).strip()

        links = {
            "1": config.DISCORD_INVITE,
            "2": config.GITHUB_URL,
            "3": config.GUNSLOL_URL,
        }

        if choice == "0" or choice == "":
            return

        if choice in links:
            webbrowser.open(
                links[choice]
            )

            return
