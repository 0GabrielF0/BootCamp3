
import pytest

from app.validator import validar_placa


@pytest.mark.parametrize(
    ("placa", "padrao_esperado"),
    [
        ("ABC-1234", "Antigo"),
        ("ABC1D23", "Mercosul"),
        ("abc-1234", "Antigo"),
        ("abc1d23", "Mercosul"),
        (" ABC1D23 ", "Mercosul"),
    ],
)
def test_placas_validas(placa, padrao_esperado):
    resultado = validar_placa(placa)

    assert resultado["valida"] is True
    assert resultado["padrao"] == padrao_esperado
    assert resultado["placa_normalizada"] == placa.strip().upper()


@pytest.mark.parametrize(
    "placa",
    [
        "AB-1234",
        "ABCD-1234",
        "ABC1234",
        "ABC-123",
        "ABC-12345",
        "ABC123D",
        "ABC@123",
        "",
        "   ",
    ],
)
def test_placas_invalidas(placa):
    resultado = validar_placa(placa)

    assert resultado["valida"] is False
    assert resultado["padrao"] is None
    assert resultado["mensagem"] == "Formato de placa inválido"
