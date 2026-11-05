
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_rota_inicial():
    # CT-44, RF-11
    resposta = client.get("/")

    assert resposta.status_code == 200
    assert "text/html" in resposta.headers["content-type"]
    assert "PlacaCheck" in resposta.text
    assert resposta.text.lower().startswith("<!doctype html>")


def test_arquivos_estaticos_da_interface():
    # CT-45, RF-11
    for caminho in ("/static/style.css", "/static/script.js"):
        assert client.get(caminho).status_code == 200


def test_interface_nao_converte_letras():
    # RF-11, RN-03.3: a normalização é feita somente pela API
    assert "toUpperCase" not in client.get("/static/script.js").text


def test_api_nao_transcreve_caracteres_fora_de_ascii():
    # CT-47, RN-03.3
    resposta = client.post("/validar", json={"placa": "ſbc1234"})

    assert resposta.status_code == 200
    assert resposta.json()["valida"] is False
    assert resposta.json()["motivo"] == "CARACTERE_INVALIDO"


def test_documentacao_openapi():
    # RNF-08
    assert client.get("/docs").status_code == 200
    assert client.get("/openapi.json").status_code == 200


def test_health():
    # CT-41, RF-10
    resposta = client.get("/health")

    assert resposta.status_code == 200
    assert resposta.json() == {"status": "ok"}


def test_api_placa_antiga():
    # CT-34, RF-07
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
    # RN-03.1, RF-05
    resposta = client.post("/validar", json={"placa": "ABC1234"})

    assert resposta.status_code == 200
    assert resposta.json()["valida"] is True
    assert resposta.json()["placa_normalizada"] == "ABC1234"


def test_api_placa_mercosul():
    # RF-02, RF-04
    resposta = client.post("/validar", json={"placa": "ABC1D23"})

    assert resposta.status_code == 200
    assert resposta.json()["valida"] is True
    assert resposta.json()["padrao"] == "mercosul"


def test_api_placa_invalida():
    # RF-06, RN-08
    resposta = client.post("/validar", json={"placa": "ABC!234"})

    assert resposta.status_code == 200
    assert resposta.json()["valida"] is False
    assert resposta.json()["motivo"] == "CARACTERE_INVALIDO"


def test_api_formato_desconhecido():
    # RF-06, RN-09
    resposta = client.post("/validar", json={"placa": "1234ABC"})

    assert resposta.status_code == 200
    assert resposta.json()["motivo"] == "FORMATO_DESCONHECIDO"


def test_api_campo_ausente():
    # CT-37, RF-08
    resposta = client.post("/validar", json={})

    assert resposta.status_code == 422
    assert resposta.json()["erro"]["codigo"] == "REQUISICAO_INVALIDA"


def test_api_tipo_incorreto():
    # CT-38, RF-08
    resposta = client.post("/validar", json={"placa": 12345})

    assert resposta.status_code == 422
    assert resposta.json()["erro"]["codigo"] == "REQUISICAO_INVALIDA"


def test_api_rota_antiga_nao_existe():
    # CT-43, RF-07
    resposta = client.post("/validate", json={"placa": "ABC-1234"})

    assert resposta.status_code == 404


def test_get_validar_metodo_nao_permitido():
    # CT-40
    resposta = client.get("/validar")

    assert resposta.status_code == 405
    assert resposta.json()["erro"]["codigo"] == "METODO_NAO_PERMITIDO"


def test_api_placa_curta_xxx():
    # CT-35
    resposta = client.post("/validar", json={"placa": "XXX"})

    assert resposta.status_code == 200
    assert resposta.json()["valida"] is False


def test_api_campo_com_nome_errado():
    # CT-36, RF-08
    resposta = client.post("/validar", json={"plaka": "ABC1234"})

    assert resposta.status_code == 422
    assert resposta.json()["erro"] == {
        "codigo": "REQUISICAO_INVALIDA",
        "mensagem": "Corpo da requisição inválido.",
        "detalhes": [
            {"campo": "placa", "problema": "Campo obrigatório ausente."},
        ],
    }


def test_api_corpo_nao_json():
    # CT-39, RF-08
    resposta = client.post(
        "/validar",
        content="ABC1234",
        headers={"Content-Type": "text/plain"},
    )

    assert resposta.status_code == 422
    assert resposta.json()["erro"]["codigo"] == "REQUISICAO_INVALIDA"
