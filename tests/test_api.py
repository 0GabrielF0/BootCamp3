
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_rota_inicial():
    resposta = client.get("/")

    assert resposta.status_code == 200
    assert resposta.json()["status"] == "operacional"


def test_health():
    resposta = client.get("/health")

    assert resposta.status_code == 200
    assert resposta.json() == {"status": "ok"}


def test_api_placa_antiga():
    resposta = client.post("/validar", json={"placa": "ABC-1234"})

    assert resposta.status_code == 200
    assert resposta.json() == {
        "valida": True,
        "placa_normalizada": "ABC1234",
        "padrao": "antigo",
        "motivo": None,
        "mensagem": "Placa válida no padrão antigo.",
    }


def test_api_placa_antiga_sem_hifen():
    resposta = client.post("/validar", json={"placa": "ABC1234"})

    assert resposta.status_code == 200
    assert resposta.json()["valida"] is True
    assert resposta.json()["placa_normalizada"] == "ABC1234"


def test_api_placa_mercosul():
    resposta = client.post("/validar", json={"placa": "ABC1D23"})

    assert resposta.status_code == 200
    assert resposta.json()["valida"] is True
    assert resposta.json()["padrao"] == "mercosul"


def test_api_placa_invalida():
    resposta = client.post("/validar", json={"placa": "ABC!234"})

    assert resposta.status_code == 200
    assert resposta.json()["valida"] is False
    assert resposta.json()["motivo"] == "CARACTERE_INVALIDO"


def test_api_formato_desconhecido():
    resposta = client.post("/validar", json={"placa": "1234ABC"})

    assert resposta.status_code == 200
    assert resposta.json()["motivo"] == "FORMATO_DESCONHECIDO"


def test_api_campo_ausente():
    resposta = client.post("/validar", json={})

    assert resposta.status_code == 422
    assert resposta.json()["erro"]["codigo"] == "REQUISICAO_INVALIDA"


def test_api_tipo_incorreto():
    resposta = client.post("/validar", json={"placa": 12345})

    assert resposta.status_code == 422
    assert resposta.json()["erro"]["codigo"] == "REQUISICAO_INVALIDA"


def test_api_rota_antiga_nao_existe():
    resposta = client.post("/validate", json={"placa": "ABC-1234"})

    assert resposta.status_code == 404


def test_get_validar_metodo_nao_permitido():
    resposta = client.get("/validar")

    assert resposta.status_code == 405
    assert resposta.json()["erro"]["codigo"] == "METODO_NAO_PERMITIDO"
