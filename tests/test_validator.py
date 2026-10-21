
import pytest

from app.core.normalizador import normalizar
from app.core.resultado import Motivo, Padrao
from app.core.validador import validar_placa


@pytest.mark.parametrize(
    ("entrada", "normalizada", "padrao"),
    [
        ("ABC-1234", "ABC1234", Padrao.ANTIGO),
        ("ABC1234", "ABC1234", Padrao.ANTIGO),
        (" abc-1234 ", "ABC1234", Padrao.ANTIGO),
        ("abc1234", "ABC1234", Padrao.ANTIGO),
        ("ABC1D23", "ABC1D23", Padrao.MERCOSUL),
        ("abc1d23", "ABC1D23", Padrao.MERCOSUL),
        ("ABC-1D23", "ABC1D23", Padrao.MERCOSUL),
        ("AAA0A00", "AAA0A00", Padrao.MERCOSUL),
        ("ZZZ9Z99", "ZZZ9Z99", Padrao.MERCOSUL),
        ("AAA-0000", "AAA0000", Padrao.ANTIGO),
        ("ZZZ-9999", "ZZZ9999", Padrao.ANTIGO),
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
        (None, Motivo.ENTRADA_NULA),
        (1234567, Motivo.TIPO_INVALIDO),
        (["ABC1234"], Motivo.TIPO_INVALIDO),
        ("", Motivo.ENTRADA_VAZIA),
        ("   ", Motivo.ENTRADA_VAZIA),
        ("ABC123", Motivo.TAMANHO_INVALIDO),
        ("ABC12345", Motivo.TAMANHO_INVALIDO),
        ("A", Motivo.TAMANHO_INVALIDO),
        ("ABC 1234", Motivo.TAMANHO_INVALIDO),
        ("AB-C-1234", Motivo.TAMANHO_INVALIDO),
        ("ABC!234", Motivo.CARACTERE_INVALIDO),
        ("ÁBC1234", Motivo.CARACTERE_INVALIDO),
        ("ABÇ1234", Motivo.CARACTERE_INVALIDO),
        ("ABC_1234", Motivo.TAMANHO_INVALIDO),
        ("ABC12@4", Motivo.CARACTERE_INVALIDO),
        ("1234ABC", Motivo.FORMATO_DESCONHECIDO),
        ("ABCD123", Motivo.FORMATO_DESCONHECIDO),
        ("AB1C234", Motivo.FORMATO_DESCONHECIDO),
        ("ABCDEFG", Motivo.FORMATO_DESCONHECIDO),
        ("1234567", Motivo.FORMATO_DESCONHECIDO),
        ("ABC1DD3", Motivo.FORMATO_DESCONHECIDO),
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
    assert normalizar(" ABC-1234 ") == "ABC1234"


def test_normalizador_nao_remove_hifen_em_outra_posicao():
    assert normalizar("AB-C1234") == "AB-C1234"


def test_normalizador_nao_remove_hifens_adicionais():
    assert normalizar("AB-C-1234") == "AB-C-1234"


def test_nucleo_nao_depende_de_framework_web():
    from pathlib import Path

    arquivos = Path("app/core").glob("*.py")
    proibidos = ("fastapi", "pydantic", "starlette", "app.api")

    for arquivo in arquivos:
        conteudo = arquivo.read_text(encoding="utf-8").lower()
        for dependencia in proibidos:
            assert dependencia not in conteudo, (
                f"{arquivo} não deve importar ou referenciar {dependencia}"
            )
