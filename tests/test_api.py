
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_rota_inicial():
    resposta = client.get("/")

    assert resposta.status_code == 200
    assert resposta.json()["status"] == "operacional"


def test_api_placa_antiga():
    resposta = client.post(
        "/validate",
        json={"placa": "ABC-1234"}
    )

    assert resposta.status_code == 200
    assert resposta.json()["valida"] is True
    assert resposta.json()["padrao"] == "Antigo"


def test_api_placa_mercosul():
    resposta = client.post(
        "/validate",
        json={"placa": "ABC1D23"}
    )

    assert resposta.status_code == 200
    assert resposta.json()["valida"] is True
    assert resposta.json()["padrao"] == "Mercosul"


def test_api_placa_invalida():
    resposta = client.post(
        "/validate",
        json={"placa": "ABC1234"}
    )

    assert resposta.status_code == 200
    assert resposta.json()["valida"] is False


def test_api_campo_ausente():
    resposta = client.post("/validate", json={})

    assert resposta.status_code == 422


def test_api_tipo_incorreto():
    resposta = client.post(
        "/validate",
        json={"placa": 12345}
    )

    assert resposta.status_code == 422
