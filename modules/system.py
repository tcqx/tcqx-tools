import platform
import time
import datetime

from core import ui, animations, config
from core.utils import get_hostname, human_bytes

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False


def _get_cpu_info():
    info = {"Modele": platform.processor() or "N/A"}
    if PSUTIL_AVAILABLE:
        try:
            info["Coeurs physiques"] = psutil.cpu_count(logical=False) or "N/A"
            info["Coeurs logiques"] = psutil.cpu_count(logical=True) or "N/A"
            info["Utilisation"] = f"{psutil.cpu_percent(interval=0.3)} %"
        except Exception:
            pass
    else:
        info["Details"] = "Installez 'psutil' pour plus de details (pip install psutil)"
    return info


def _get_ram_info():
    if not PSUTIL_AVAILABLE:
        return {"RAM": "psutil non installe -- information indisponible"}
    try:
        mem = psutil.virtual_memory()
        return {
            "Totale": human_bytes(mem.total),
            "Utilisee": human_bytes(mem.used),
            "Disponible": human_bytes(mem.available),
            "Utilisation": f"{mem.percent} %",
        }
    except Exception:
        return {"RAM": "Information indisponible"}


def _get_disk_info():
    if not PSUTIL_AVAILABLE:
        return {"Disque": "psutil non installe -- information indisponible"}
    try:
        usage = psutil.disk_usage("/")
        return {
            "Total": human_bytes(usage.total),
            "Utilise": human_bytes(usage.used),
            "Libre": human_bytes(usage.free),
            "Utilisation": f"{usage.percent} %",
        }
    except Exception:
        return {"Disque": "Information indisponible"}


def _get_uptime():
    if not PSUTIL_AVAILABLE:
        return "N/A (psutil non installe)"
    try:
        boot_ts = psutil.boot_time()
        uptime_seconds = time.time() - boot_ts
        delta = datetime.timedelta(seconds=int(uptime_seconds))
        return str(delta)
    except Exception:
        return "N/A"


def run(console):
    ui.print_module_header(console, "System // Informations systeme")
    animations.loading_bar(console, "Collecte des informations systeme", duration=0.5)

    general_rows = {
        "OS": f"{platform.system()} {platform.release()}",
        "Version detaillee": platform.version(),
        "Architecture": platform.machine(),
        "Python": platform.python_version(),
        "Hostname": get_hostname(),
        "Uptime": _get_uptime(),
    }
    ui.info_panel(console, "GENERAL", general_rows)
    console.print()

    ui.info_panel(console, "CPU", _get_cpu_info())
    console.print()

    ui.info_panel(console, "RAM", _get_ram_info())
    console.print()

    ui.info_panel(console, "DISQUE", _get_disk_info())

    console.print()
    animations.print_ok(console, "Collecte systeme terminee.")
    ui.press_enter(console)
