
from time import perf_counter

import pytest

from app.core.normalizador import normalizar
from app.core.resultado import Motivo, Padrao
from app.core.validador import validar_placa


@pytest.mark.parametrize(
    ("entrada", "normalizada", "padrao"),
    [
        ("ABC-1234", "ABC1234", Padrao.ANTIGO),  # CT-01, RF-01
        ("ABC1234", "ABC1234", Padrao.ANTIGO),  # CT-02
        ("abc-1234", "ABC1234", Padrao.ANTIGO),  # CT-03, RF-03
        ("  ABC-1234  ", "ABC1234", Padrao.ANTIGO),  # CT-04
        (" abc1234 ", "ABC1234", Padrao.ANTIGO),  # CT-05
        (" abc-1234 ", "ABC1234", Padrao.ANTIGO),  # RF-03
        ("abc1234", "ABC1234", Padrao.ANTIGO),  # RN-03
        ("ABC1D23", "ABC1D23", Padrao.MERCOSUL),  # CT-06, RF-02
        ("abc1d23", "ABC1D23", Padrao.MERCOSUL),  # CT-07
        ("ABC-1D23", "ABC1D23", Padrao.MERCOSUL),  # CT-08
        ("AAA0A00", "AAA0A00", Padrao.MERCOSUL),  # CT-09
        ("ZZZ9Z99", "ZZZ9Z99", Padrao.MERCOSUL),  # CT-10
        ("AAA-0000", "AAA0000", Padrao.ANTIGO),  # CT-11
        ("ZZZ-9999", "ZZZ9999", Padrao.ANTIGO),  # CT-12
    ],
)
def test_placas_validas(entrada, normalizada, padrao):
    resultado = validar_placa(entrada)

    assert resultado.valida is True
    assert resultado.placa_normalizada == normalizada
    assert resultado.padrao == padrao
    assert resultado.motivo is None


@pytest.mark.parametrize(
    ("entrada", "motivo"),
    [
        (None, Motivo.ENTRADA_NULA),  # CT-13, RN-04
        (1234567, Motivo.TIPO_INVALIDO),  # CT-14, RN-05
        (["ABC1234"], Motivo.TIPO_INVALIDO),  # CT-15, RN-05
        ("", Motivo.ENTRADA_VAZIA),  # CT-16, RN-06
        ("   ", Motivo.ENTRADA_VAZIA),  # CT-17, RN-06
        ("ABC123", Motivo.TAMANHO_INVALIDO),  # CT-18, RN-07
        ("ABC12345", Motivo.TAMANHO_INVALIDO),  # CT-19, RN-07
        ("A", Motivo.TAMANHO_INVALIDO),  # CT-20, RN-07
        ("ABC 1234", Motivo.TAMANHO_INVALIDO),  # CT-21, RN-03.2
        ("AB-C-1234", Motivo.TAMANHO_INVALIDO),  # CT-22, RN-11
        ("ABC!234", Motivo.CARACTERE_INVALIDO),  # CT-23, RN-08
        ("ÁBC1234", Motivo.CARACTERE_INVALIDO),  # CT-24, RN-03.3
        ("ABÇ1234", Motivo.CARACTERE_INVALIDO),  # CT-25, RN-08
        ("ABC_1234", Motivo.TAMANHO_INVALIDO),  # CT-26, RN-07
        ("ABC12@4", Motivo.CARACTERE_INVALIDO),  # CT-27, RN-08
        ("1234ABC", Motivo.FORMATO_DESCONHECIDO),  # CT-28, RN-09
        ("ABCD123", Motivo.FORMATO_DESCONHECIDO),  # CT-29, RN-09
        ("AB1C234", Motivo.FORMATO_DESCONHECIDO),  # CT-30, RN-09
        ("ABCDEFG", Motivo.FORMATO_DESCONHECIDO),  # CT-31, RN-09
        ("1234567", Motivo.FORMATO_DESCONHECIDO),  # CT-32, RN-09
        ("ABC1DD3", Motivo.FORMATO_DESCONHECIDO),  # CT-33, RN-09
    ],
)
def test_placas_invalidas(entrada, motivo):
    resultado = validar_placa(entrada)

    assert resultado.valida is False
    assert resultado.placa_normalizada is None
    assert resultado.padrao is None
    assert resultado.motivo == motivo
    assert resultado.mensagem


def test_normalizador_remove_hifen_separador():
    # RN-03, RN-03.4
    assert normalizar(" ABC-1234 ") == "ABC1234"


def test_normalizador_nao_remove_hifen_em_outra_posicao():
    # RN-11
    assert normalizar("AB-C1234") == "AB-C1234"


def test_normalizador_nao_remove_hifens_adicionais():
    # RN-11
    assert normalizar("AB-C-1234") == "AB-C-1234"


def test_validacao_responde_em_menos_de_5_ms():
    # RNF-03: média de 1.000 validações, para não depender de uma medição isolada
    repeticoes = 1000
    inicio = perf_counter()
    for _ in range(repeticoes):
        validar_placa("ABC1D23")
    media_em_ms = (perf_counter() - inicio) * 1000 / repeticoes

    assert media_em_ms < 5


def test_nucleo_nao_depende_de_framework_web():
    # RNF-01, RF-09
    from pathlib import Path

    arquivos = Path("app/core").glob("*.py")
    proibidos = ("fastapi", "pydantic", "starlette", "app.api")

    for arquivo in arquivos:
        conteudo = arquivo.read_text(encoding="utf-8").lower()
        for dependencia in proibidos:
            assert dependencia not in conteudo, (
                f"{arquivo} não deve importar ou referenciar {dependencia}"
            )
