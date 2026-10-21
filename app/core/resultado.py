
from dataclasses import dataclass
from enum import Enum


class Padrao(str, Enum):
    ANTIGO = "antigo"
    MERCOSUL = "mercosul"


class Motivo(str, Enum):
    ENTRADA_NULA = "ENTRADA_NULA"
    TIPO_INVALIDO = "TIPO_INVALIDO"
    ENTRADA_VAZIA = "ENTRADA_VAZIA"
    TAMANHO_INVALIDO = "TAMANHO_INVALIDO"
    CARACTERE_INVALIDO = "CARACTERE_INVALIDO"
    FORMATO_DESCONHECIDO = "FORMATO_DESCONHECIDO"


@dataclass(frozen=True)
class ResultadoValidacao:
    valida: bool
    placa_normalizada: str | None
    padrao: Padrao | None
    motivo: Motivo | None
    mensagem: str
