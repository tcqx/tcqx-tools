from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich.prompt import Prompt
from rich import box

from core import config


def make_console():
    return Console(highlight=False)


def clear(console):
    console.clear()


def print_title_banner(console):
    title = Text("T C Q X", style=f"bold {config.COLOR_PRIMARY}")
    subtitle = Text(
        "T E R M I N A L  //  O N L I N E",
        style=config.COLOR_ACCENT
    )

    content = Text.assemble(
        title,
        "\n",
        subtitle
    )

    panel = Panel(
        Align.center(content),
        border_style=config.COLOR_PRIMARY,
        box=box.DOUBLE,
        padding=(1, 6)
    )

    console.print(panel)


def system_status_table():
    table = Table(
        show_header=False,
        box=None,
        padding=(0, 1)
    )

    table.add_column(style=f"bold {config.COLOR_DIM}", width=16)
    table.add_column(style=config.COLOR_PRIMARY)

    table.add_row(
        "STATUS",
        f"[bold {config.COLOR_OK}]ONLINE[/]"
    )

    table.add_row(
        "PLATFORM",
        config.IS_WINDOWS and "WINDOWS" or "OTHER"
    )

    table.add_row(
        "PYTHON",
        platform_version()
    )

    table.add_row(
        "USER",
        config.APP_USER
    )

    return table


def platform_version():
    import platform
    return platform.python_version()


def modules_table(modules):
    table = Table(
        show_header=False,
        box=None,
        padding=(0, 1)
    )

    table.add_column(
        width=7,
        style=f"bold {config.COLOR_ACCENT}"
    )

    table.add_column(
        style=config.COLOR_PRIMARY
    )

    for number, name in modules:
        if number == "00":
            table.add_row("", "")
            table.add_row(
                f"[{number}]",
                f"[{config.COLOR_DIM}]{name}[/]"
            )
        else:
            table.add_row(
                f"[{number}]",
                name
            )

    return table


def print_dashboard(console, modules):
    clear(console)

    console.print()
    print_title_banner(console)
    console.print()

    system = Panel(
        system_status_table(),
        title="[bold] SYSTEM [/]",
        title_align="left",
        border_style=config.COLOR_PANEL_BORDER,
        box=box.ROUNDED,
        padding=(1, 2)
    )

    console.print(system)
    console.print()

    menu = Panel(
        modules_table(modules),
        title="[bold] MODULES [/]",
        title_align="left",
        border_style=config.COLOR_PANEL_BORDER,
        box=box.ROUNDED,
        padding=(1, 2)
    )

    console.print(menu)
    console.print()


def print_module_header(console, title):
    clear(console)

    header = Panel(
        Align.center(
            Text(
                title.upper(),
                style=f"bold {config.COLOR_PRIMARY}"
            )
        ),
        border_style=config.COLOR_PRIMARY,
        box=box.HEAVY,
        padding=(1, 3)
    )

    console.print()
    console.print(header)
    console.print()


def info_panel(console, title, rows):
    table = Table(
        show_header=False,
        box=None,
        padding=(0, 1)
    )

    table.add_column(
        style=f"bold {config.COLOR_DIM}",
        width=18
    )

    table.add_column(
        style=config.COLOR_PRIMARY
    )

    for key, value in rows.items():
        value = value if value not in (None, "") else "N/A"
        table.add_row(key, str(value))

    panel = Panel(
        table,
        title=f"[bold {config.COLOR_ACCENT}] {title} [/]",
        border_style=config.COLOR_PANEL_BORDER,
        box=box.ROUNDED,
        padding=(1, 2)
    )

    console.print(panel)


def prompt(console, message, default=None):
    label = (
        f"[bold {config.COLOR_PRIMARY}]"
        f"tcqx@system"
        f"[{config.COLOR_DIM}]:[/]"
        f"[bold {config.COLOR_PRIMARY}]~$[/] "
        f"{message}"
    )

    try:
        if default is not None:
            return Prompt.ask(label, default=default)

        return Prompt.ask(label)

    except (EOFError, KeyboardInterrupt):
        return ""


def press_enter(
    console,
    message="Press ENTER to continue..."
):
    try:
        console.input(
            f"[{config.COLOR_DIM}]{message}[/]"
        )
    except (EOFError, KeyboardInterrupt):
        pass


def footer_prompt(console):
    try:
        return console.input(
            f"[bold {config.COLOR_PRIMARY}]"
            f"tcqx@system"
            f"[{config.COLOR_DIM}]:[/]"
            f"[bold {config.COLOR_PRIMARY}]~$[/] "
        ).strip()

    except (EOFError, KeyboardInterrupt):
        return "00"
