import os
import platform

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich.prompt import Prompt
from rich import box

from core import config
from core.utils import get_hostname, terminal_width


def make_console() -> Console:
    if config.IS_WINDOWS:
        os.system("mode con: cols=140 lines=45")

    return Console(
        highlight=False,
        width=138
    )


def clear(console: Console):
    console.clear()


def print_title_banner(console: Console):
    title = Text(
        "T C Q X",
        style=f"bold {config.COLOR_PRIMARY}",
        justify="center"
    )

    subtitle = Text(
        "TERMINAL // ONLINE",
        style=config.COLOR_ACCENT,
        justify="center"
    )

    panel = Panel(
        Align.center(
            Text.assemble(
                title,
                "\n",
                subtitle
            )
        ),
        border_style=config.COLOR_PANEL_BORDER,
        box=box.DOUBLE,
        padding=(1, 4),
    )

    console.print(panel)


def system_status_table():
    table = Table(
        show_header=False,
        box=box.SIMPLE,
        padding=(0, 1),
        border_style=config.COLOR_DIM,
    )

    table.add_column(
        style=f"bold {config.COLOR_DIM}"
    )

    table.add_column(
        style=config.COLOR_PRIMARY
    )

    table.add_row(
        "├─ STATUS",
        "[bold bright_green]ONLINE[/bold bright_green]"
    )

    table.add_row(
        "├─ PLATFORM",
        platform.system().upper()
    )

    table.add_row(
        "├─ PYTHON",
        platform.python_version()
    )

    table.add_row(
        "└─ USER",
        config.APP_USER
    )

    return table


def modules_table(modules):
    table = Table(
        show_header=False,
        box=box.SIMPLE,
        padding=(0, 1),
        border_style=config.COLOR_DIM,
    )

    table.add_column(
        style=f"bold {config.COLOR_ACCENT}",
        width=6
    )

    table.add_column(
        style=config.COLOR_PRIMARY
    )

    for number, name in modules:
        table.add_row(
            f"[{number}]",
            name
        )

    return table


def print_dashboard(console: Console, modules):
    clear(console)

    console.print()
    print_title_banner(console)
    console.print()

    console.print(
        Text(
            " SYSTEM",
            style=f"bold {config.COLOR_ACCENT}"
        )
    )

    console.print(
        system_status_table()
    )

    console.print()

    console.print(
        Text(
            " MODULES",
            style=f"bold {config.COLOR_ACCENT}"
        )
    )

    console.print(
        modules_table(modules)
    )

    console.print()


def print_module_header(console: Console, title: str):
    clear(console)

    console.print()

    header = Panel(
        Align.center(
            Text(
                title.upper(),
                style=f"bold {config.COLOR_PRIMARY}"
            )
        ),
        border_style=config.COLOR_PANEL_BORDER,
        box=box.HEAVY,
        padding=(0, 2),
    )

    console.print(header)
    console.print()


def info_panel(console, title: str, rows: dict):
    table = Table(
        show_header=False,
        box=box.SIMPLE,
        border_style=config.COLOR_DIM
    )

    table.add_column(
        style=f"bold {config.COLOR_DIM}"
    )

    table.add_column(
        style=config.COLOR_PRIMARY
    )

    for key, value in rows.items():
        table.add_row(
            key,
            str(value) if value not in (None, "") else "N/A"
        )

    panel = Panel(
        table,
        title=f"[bold {config.COLOR_ACCENT}]{title}[/bold {config.COLOR_ACCENT}]",
        border_style=config.COLOR_PANEL_BORDER,
        box=box.ROUNDED,
    )

    console.print(panel)


def prompt(
    console,
    message: str,
    default: str = None
) -> str:

    label = (
        f"[bold {config.COLOR_PRIMARY}]"
        f"tcqx@system:~$"
        f"[/bold {config.COLOR_PRIMARY}] "
        f"{message}"
    )

    try:
        if default is not None:
            return Prompt.ask(
                label,
                default=default
            )

        return Prompt.ask(label)

    except (EOFError, KeyboardInterrupt):
        return ""


def press_enter(
    console,
    message: str = "Appuyez sur ENTREE pour continuer..."
):
    try:
        console.input(
            f"[{config.COLOR_DIM}]{message}[/]"
        )

    except (EOFError, KeyboardInterrupt):
        pass


def footer_prompt(console) -> str:
    try:
        return console.input(
            f"[bold {config.COLOR_PRIMARY}]"
            f"tcqx@system:~$"
            f"[/bold {config.COLOR_PRIMARY}] "
        ).strip()

    except (EOFError, KeyboardInterrupt):
        return "00"
