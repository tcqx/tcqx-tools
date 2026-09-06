#!/usr/bin/env python3

import sys

from rich.panel import Panel
from rich.text import Text
from rich import box

from core import ui, animations, config
from modules import network, dns, system, osint, discord, utilities


MODULES = [
    ("01", "Network"),
    ("02", "DNS"),
    ("03", "System"),
    ("04", "OSINT"),
    ("05", "Links"),
    ("06", "Utilities"),
    ("07", "About"),
    ("00", "Exit"),
]


def show_about(console):
    ui.print_module_header(console, "About // TCQX Terminal")

    body = Text()

    body.append(
        f"{config.APP_FULL_NAME}\n",
        style=f"bold {config.COLOR_PRIMARY}"
    )

    body.append(
        f"Version {config.APP_VERSION}\n\n",
        style=config.COLOR_DIM
    )

    body.append(
        "Terminal utility tool made for network, system,\n"
        "OSINT and other useful tools.\n\n",
        style=config.COLOR_SECONDARY
    )

    body.append("GitHub   : ", style=config.COLOR_DIM)
    body.append(
        f"{config.GITHUB_URL}\n",
        style=config.COLOR_ACCENT
    )

    body.append("Guns.lol : ", style=config.COLOR_DIM)
    body.append(
        f"{config.GUNSLOL_URL}\n",
        style=config.COLOR_ACCENT
    )

    body.append("Discord  : ", style=config.COLOR_DIM)
    body.append(
        f"{config.DISCORD_INVITE}\n",
        style=config.COLOR_ACCENT
    )

    console.print(
        Panel(
            body,
            border_style=config.COLOR_PANEL_BORDER,
            box=box.ROUNDED
        )
    )

    console.print()
    ui.press_enter(console)


def run_module(console, choice):
    modules = {
        "01": ("Network", network.run),
        "02": ("DNS", dns.run),
        "03": ("System", system.run),
        "04": ("OSINT", osint.run),
        "05": ("Links", discord.run),
        "06": ("Utilities", utilities.run),
        "07": ("About", show_about),
    }

    module = modules.get(choice)

    if module is None:
        animations.print_error(
            console,
            "Unknown option."
        )

        ui.press_enter(
            console,
            "Press ENTER to continue..."
        )

        return

    name, function = module

    animations.transition_to(
        console,
        name
    )

    function(console)


def main():
    console = ui.make_console()

    try:
        animations.boot_sequence(console)

        while True:
            ui.print_dashboard(
                console,
                MODULES
            )

            choice = ui.footer_prompt(
                console
            ).strip().lower()

            if choice in ("00", "exit", "quit"):
                console.print()

                animations.typing_effect(
                    console,
                    "Closing TCQX Terminal...",
                    style=config.COLOR_SECONDARY
                )

                animations.print_ok(
                    console,
                    "See you soon."
                )

                break

            run_module(
                console,
                choice
            )

    except KeyboardInterrupt:
        console.print()

        animations.print_error(
            console,
            "Interrupted."
        )

        sys.exit(0)

    except Exception as exc:
        console.print()

        animations.print_error(
            console,
            f"Error: {exc}"
        )

        sys.exit(1)


if __name__ == "__main__":
    main()
