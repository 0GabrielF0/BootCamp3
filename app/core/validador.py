
import re

from app.core.normalizador import normalizar
from app.core.resultado import Motivo, Padrao, ResultadoValidacao


PADRAO_ANTIGO = re.compile(r"^[A-Z]{3}[0-9]{4}$")
PADRAO_MERCOSUL = re.compile(r"^[A-Z]{3}[0-9][A-Z][0-9]{2}$")
CARACTERES_PERMITIDOS = re.compile(r"^[A-Z0-9]+$")


def _rejeitar(motivo: Motivo, mensagem: str) -> ResultadoValidacao:
    return ResultadoValidacao(
        valida=False,
        placa_normalizada=None,
        padrao=None,
        motivo=motivo,
        mensagem=mensagem,
    )


def validar_placa(entrada: object) -> ResultadoValidacao:
    """Valida uma placa conforme RN-01 a RN-12; não lança erro para entradas comuns."""

    # RN-04: entrada nula
    if entrada is None:
        return _rejeitar(
            Motivo.ENTRADA_NULA,
            "A entrada da placa não pode ser nula.",
        )

    # RN-05: tipo incorreto
    if not isinstance(entrada, str):
        return _rejeitar(
            Motivo.TIPO_INVALIDO,
            "A placa deve ser informada como texto.",
        )

    # RN-06: vazia ou somente espaços
    if not entrada.strip():
        return _rejeitar(
            Motivo.ENTRADA_VAZIA,
            "A placa não pode estar vazia.",
        )

    placa = normalizar(entrada)

    # RN-07: tamanho diferente de sete caracteres
    if len(placa) != 7:
        return _rejeitar(
            Motivo.TAMANHO_INVALIDO,
            "A placa deve possuir exatamente 7 caracteres após a normalização.",
        )

    # RN-08: caracteres fora de A-Z e 0-9
    if not CARACTERES_PERMITIDOS.fullmatch(placa):
        return _rejeitar(
            Motivo.CARACTERE_INVALIDO,
            "A placa contém caracteres não permitidos. Use apenas letras de A a Z e dígitos de 0 a 9.",
        )

    # RN-01: padrão antigo
    if PADRAO_ANTIGO.fullmatch(placa):
        return ResultadoValidacao(
            valida=True,
            placa_normalizada=placa,
            padrao=Padrao.ANTIGO,
            motivo=None,
            mensagem="Placa válida no padrão antigo.",
        )

    # RN-02: padrão Mercosul
    if PADRAO_MERCOSUL.fullmatch(placa):
        return ResultadoValidacao(
            valida=True,
            placa_normalizada=placa,
            padrao=Padrao.MERCOSUL,
            motivo=None,
            mensagem="Placa válida no padrão Mercosul.",
        )

    # RN-09: sete caracteres alfanuméricos, mas máscara desconhecida
    return _rejeitar(
        Motivo.FORMATO_DESCONHECIDO,
        "A placa não corresponde ao padrão antigo nem ao padrão Mercosul.",
    )
