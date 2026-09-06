import subprocess
import platform
import socket
import shutil


def safe_run(command, timeout=5):
    """
    Execute une commande systeme de maniere securisee et retourne sa sortie.
    Ne leve jamais d'exception : retourne None en cas d'echec.
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except Exception:
        return None


def human_bytes(num_bytes):
    """Convertit un nombre d'octets en une chaine lisible (Ko, Mo, Go...)."""
    try:
        num_bytes = float(num_bytes)
    except (TypeError, ValueError):
        return "N/A"

    for unit in ["o", "Ko", "Mo", "Go", "To", "Po"]:
        if abs(num_bytes) < 1024.0:
            return f"{num_bytes:3.1f} {unit}"
        num_bytes /= 1024.0
    return f"{num_bytes:.1f} Eo"


def get_hostname():
    try:
        return socket.gethostname()
    except Exception:
        return "N/A"


def get_local_ip():
    """Recupere l'IP locale principale sans envoyer de trafic reseau reel."""
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(1)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        return ip
    except Exception:
        return "N/A"
    finally:
        if s:
            s.close()


def terminal_width(default=80):
    try:
        return shutil.get_terminal_size((default, 24)).columns
    except Exception:
        return default


def is_tool_available(name):
    """Verifie si un executable est disponible dans le PATH."""
    return shutil.which(name) is not None


def platform_name():
    return platform.system()
