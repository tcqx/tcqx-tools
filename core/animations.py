import time
import sys
import random

from rich.console import Console
from rich.text import Text
from rich.progress import (
    Progress,
    BarColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.align import Align

from core import config


def typing_effect(console: Console, text: str, style: str = None, delay: float = 0.012):
    """Affiche du texte caractere par caractere pour un effet 'terminal'."""
    style = style or config.COLOR_PRIMARY
    for char in text:
        console.print(char, style=style, end="")
        sys.stdout.flush()
        time.sleep(delay)
    console.print()


def boot_line(console: Console, tag: str, message: str, delay: float = 0.25):
    """Affiche une ligne de boot du type '[ SYSTEM ] initializing...'."""
    line = Text()
    line.append("[ ", style=config.COLOR_DIM)
    line.append(f"{tag:<7}", style=f"bold {config.COLOR_ACCENT}")
    line.append(" ] ", style=config.COLOR_DIM)
    line.append(message, style=config.COLOR_SECONDARY)
    console.print(line)
    time.sleep(delay)


def boot_sequence(console: Console):
    """Sequence d'amorcage affichee au lancement du programme."""
    console.clear()
    console.print()

    boot_lines = [
        ("SYSTEM", "initializing..."),
        ("CORE", "loading modules..."),
        ("NETWORK", "checking interface..."),
        ("UI", "starting terminal..."),
    ]

    for tag, message in boot_lines:
        boot_line(console, tag, message, delay=random.uniform(0.18, 0.35))

    time.sleep(0.2)

    with Progress(
        TextColumn("[bold green]BOOT[/bold green]"),
        BarColumn(bar_width=40, style=config.COLOR_DIM, complete_style=config.COLOR_PRIMARY),
        TextColumn("[green]{task.percentage:>3.0f}%[/green]"),
        TimeElapsedColumn(),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task("boot", total=100)
        while not progress.finished:
            progress.update(task, advance=random.uniform(4, 12))
            time.sleep(0.03)

    console.print()
    reveal_logo(console)
    time.sleep(0.4)


def reveal_logo(console: Console):
    """Fait apparaitre le logo ASCII TCQX ligne par ligne."""
    lines = config.ASCII_LOGO.strip("\n").split("\n")
    for line in lines:
        console.print(Align.center(Text(line, style=f"bold {config.COLOR_PRIMARY}")))
        time.sleep(0.04)


def loading_bar(console: Console, description: str = "Chargement", duration: float = 0.6):
    """Petite barre de progression generique reutilisable dans les modules."""
    with Progress(
        TextColumn(f"[{config.COLOR_SECONDARY}]{{task.description}}[/{config.COLOR_SECONDARY}]"),
        BarColumn(bar_width=30, style=config.COLOR_DIM, complete_style=config.COLOR_PRIMARY),
        TextColumn("[green]{task.percentage:>3.0f}%[/green]"),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task(description, total=100)
        steps = 20
        for _ in range(steps):
            progress.update(task, advance=100 / steps)
            time.sleep(duration / steps)


def spinner(console: Console, message: str, duration: float = 0.8):
    """Affiche un spinner pendant une courte duree (operation en cours)."""
    frames = ["|", "/", "-", "\\"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        frame = frames[i % len(frames)]
        console.print(f"\r[{config.COLOR_ACCENT}]{frame}[/] {message}", end="")
        sys.stdout.flush()
        time.sleep(0.08)
        i += 1
    console.print("\r" + " " * (len(message) + 4), end="\r")


def scan_effect(console: Console, width: int = 50):
    """Petit effet de 'scan' horizontal, esthetique cyberpunk."""
    for i in range(0, width, 5):
        bar = "─" * i + "█" + "─" * (width - i)
        console.print(f"[{config.COLOR_DIM}]{bar}[/]", end="\r")
        time.sleep(0.015)
    console.print(" " * (width + 2), end="\r")


def print_ok(console: Console, message: str):
    """Notification standard de succes : '[ OK ] message'."""
    line = Text()
    line.append("[ ", style=config.COLOR_DIM)
    line.append("OK", style=f"bold {config.COLOR_OK}")
    line.append(" ] ", style=config.COLOR_DIM)
    line.append(message, style=config.COLOR_SECONDARY)
    console.print(line)


def print_error(console: Console, message: str):
    """Notification standard d'erreur : '[ ERR ] message'."""
    line = Text()
    line.append("[ ", style=config.COLOR_DIM)
    line.append("ERR", style=f"bold {config.COLOR_ERROR}")
    line.append(" ] ", style=config.COLOR_DIM)
    line.append(message, style=config.COLOR_WARNING)
    console.print(line)


def transition_to(console: Console, title: str):
    """Petite transition animee lors du changement de menu."""
    scan_effect(console, width=min(60, 40))
    console.print(f"[{config.COLOR_DIM}]>> {title}[/]")
    time.sleep(0.15)
