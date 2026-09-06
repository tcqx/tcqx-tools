import base64
import hashlib
import os
import secrets
import string
import uuid
import ast
import operator
import time

from core import ui, animations, config
from core.utils import human_bytes


_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _safe_eval(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value

        raise ValueError("Valeur non numerique interdite.")

    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPERATORS:
        return _ALLOWED_OPERATORS[type(node.op)](
            _safe_eval(node.left),
            _safe_eval(node.right)
        )

    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPERATORS:
        return _ALLOWED_OPERATORS[type(node.op)](
            _safe_eval(node.operand)
        )

    raise ValueError("Expression non autorisee.")


def safe_calculate(expression: str):
    tree = ast.parse(expression, mode="eval")
    return _safe_eval(tree.body)


def _generate_password(console):
    length_str = ui.prompt(
        console,
        "Longueur du mot de passe (defaut 16) > ",
        default="16"
    )

    try:
        length = max(4, min(128, int(length_str)))
    except ValueError:
        length = 16

    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    password = "".join(
        secrets.choice(alphabet)
        for _ in range(length)
    )

    console.print()

    ui.info_panel(
        console,
        "MOT DE PASSE GENERE",
        {
            "Mot de passe": password,
            "Longueur": length
        }
    )

    console.print()
    animations.print_ok(console, "Mot de passe genere.")
    ui.press_enter(console)


def _generate_uuid(console):
    generated = str(uuid.uuid4())

    console.print()

    ui.info_panel(
        console,
        "UUID GENERE",
        {
            "UUID v4": generated
        }
    )

    console.print()
    animations.print_ok(console, "UUID genere.")
    ui.press_enter(console)


def _base64_tool(console):
    mode = ui.prompt(
        console,
        "Encoder ou decoder ? (encode/decode) > ",
        default="encode"
    ).lower()

    text = ui.prompt(console, "Texte > ")

    console.print()

    try:
        if mode.startswith("d"):
            result = base64.b64decode(
                text.encode()
            ).decode(errors="replace")

            ui.info_panel(
                console,
                "BASE64 -- DECODE",
                {
                    "Resultat": result
                }
            )
        else:
            result = base64.b64encode(
                text.encode()
            ).decode()

            ui.info_panel(
                console,
                "BASE64 -- ENCODE",
                {
                    "Resultat": result
                }
            )

        animations.print_ok(console, "Operation terminee.")

    except Exception:
        animations.print_error(console, "Texte Base64 invalide.")

    ui.press_enter(console)


def _sha256_tool(console):
    text = ui.prompt(console, "Texte a hasher > ")

    digest = hashlib.sha256(
        text.encode()
    ).hexdigest()

    console.print()

    ui.info_panel(
        console,
        "HASH SHA256",
        {
            "Texte": text,
            "SHA256": digest
        }
    )

    console.print()
    animations.print_ok(console, "Hash calcule.")
    ui.press_enter(console)


def _calculator_tool(console):
    expression = ui.prompt(
        console,
        "Expression (ex: 12*(3+4)) > "
    )

    console.print()

    try:
        result = safe_calculate(expression)

        ui.info_panel(
            console,
            "CALCULATRICE",
            {
                "Expression": expression,
                "Resultat": result
            }
        )

        animations.print_ok(console, "Calcul effectue.")

    except Exception:
        animations.print_error(
            console,
            "Expression invalide ou non autorisee."
        )

    ui.press_enter(console)


def _file_info_tool(console):
    path = ui.prompt(
        console,
        "Chemin du fichier > "
    ).strip().strip('"')

    console.print()

    if not path or not os.path.exists(path):
        animations.print_error(
            console,
            "Fichier introuvable."
        )
        ui.press_enter(console)
        return

    try:
        stats = os.stat(path)

        rows = {
            "Chemin": os.path.abspath(path),
            "Taille": human_bytes(stats.st_size),
            "Derniere modification": time.strftime(
                "%Y-%m-%d %H:%M:%S",
                time.localtime(stats.st_mtime)
            ),
            "Type": "Dossier" if os.path.isdir(path) else "Fichier",
        }

        ui.info_panel(
            console,
            "INFORMATIONS FICHIER",
            rows
        )

        animations.print_ok(
            console,
            "Informations recuperees."
        )

    except Exception:
        animations.print_error(
            console,
            "Impossible de lire les informations du fichier."
        )

    ui.press_enter(console)


def _menu(console):
    ui.print_module_header(
        console,
        "Utilities // Outils divers"
    )

    console.print(
        f" [{config.COLOR_ACCENT}][1][/] Generateur de mot de passe"
    )

    console.print(
        f" [{config.COLOR_ACCENT}][2][/] Generateur UUID"
    )

    console.print(
        f" [{config.COLOR_ACCENT}][3][/] Encode / Decode Base64"
    )

    console.print(
        f" [{config.COLOR_ACCENT}][4][/] Hash SHA256"
    )

    console.print(
        f" [{config.COLOR_ACCENT}][5][/] Calculatrice"
    )

    console.print(
        f" [{config.COLOR_ACCENT}][6][/] Informations sur un fichier"
    )

    console.print(
        f" [{config.COLOR_ACCENT}][0][/] Retour"
    )

    console.print()

    return ui.prompt(console, "Choix > ")


def run(console):
    while True:
        choice = _menu(console)

        if choice == "1":
            _generate_password(console)

        elif choice == "2":
            _generate_uuid(console)

        elif choice == "3":
            _base64_tool(console)

        elif choice == "4":
            _sha256_tool(console)

        elif choice == "5":
            _calculator_tool(console)

        elif choice == "6":
            _file_info_tool(console)

        elif choice == "0" or choice == "":
            return

        else:
            animations.print_error(
                console,
                "Choix invalide."
            )
            ui.press_enter(console)
