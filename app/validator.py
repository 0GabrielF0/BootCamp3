
import re

PADRAO_ANTIGO = re.compile(r"^[A-Z]{3}-[0-9]{4}$")
PADRAO_MERCOSUL = re.compile(r"^[A-Z]{3}[0-9][A-Z][0-9]{2}$")


def normalizar_placa(placa: str) -> str:
    """Normaliza a placa sem alterar seu formato estrutural."""
    return placa.strip().upper()


def validar_placa(placa: str) -> dict:
    """Valida uma placa e identifica seu padrão."""

    placa_normalizada = normalizar_placa(placa)

    if PADRAO_ANTIGO.fullmatch(placa_normalizada):
        return {
            "placa_original": placa,
            "placa_normalizada": placa_normalizada,
            "valida": True,
            "padrao": "Antigo",
            "mensagem": "Placa válida"
        }

    if PADRAO_MERCOSUL.fullmatch(placa_normalizada):
        return {
            "placa_original": placa,
            "placa_normalizada": placa_normalizada,
            "valida": True,
            "padrao": "Mercosul",
            "mensagem": "Placa válida"
        }

    return {
        "placa_original": placa,
        "placa_normalizada": placa_normalizada,
        "valida": False,
        "padrao": None,
        "mensagem": "Formato de placa inválido"
    }
