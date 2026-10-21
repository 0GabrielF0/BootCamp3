from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.validador import validar_placa
from app.schemas import (
    ValidarPlacaRequest,
    ValidarPlacaResponse,
)

app = FastAPI(
    title="Validador de Placas Brasileiras",
    description=(
        "API para validar os padrões antigo e Mercosul "
        "de placas brasileiras."
    ),
    version="1.0.0",
)


@app.get("/")
def inicio():
    return {
        "projeto": "Validador de Placas Brasileiras",
        "status": "operacional",
        "documentacao": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/validar", response_model=ValidarPlacaResponse)
def validar(dados: ValidarPlacaRequest):
    resultado = validar_placa(dados.placa)

    return {
        "valida": resultado.valida,
        "placa_normalizada": resultado.placa_normalizada,
        "padrao": resultado.padrao.value if resultado.padrao else None,
        "motivo": resultado.motivo.value if resultado.motivo else None,
        "mensagem": resultado.mensagem,
    }


@app.exception_handler(RequestValidationError)
async def erro_validacao_requisicao(
    request: Request,
    exc: RequestValidationError,
):
    detalhes = []

    for erro in exc.errors():
        local = erro.get("loc", ())
        campo = str(local[-1]) if local else "corpo"

        if erro.get("type") == "missing":
            problema = "Campo obrigatório ausente."
        elif erro.get("type") == "json_invalid":
            problema = "O corpo da requisição não contém JSON válido."
        else:
            problema = "Valor ou tipo de dado inválido."

        detalhes.append({
            "campo": campo,
            "problema": problema,
        })

    return JSONResponse(
        status_code=422,
        content={
            "erro": {
                "codigo": "REQUISICAO_INVALIDA",
                "mensagem": "Corpo da requisição inválido.",
                "detalhes": detalhes,
            }
        },
    )




@app.exception_handler(StarletteHTTPException)
async def erro_http(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 405:
        codigo = "METODO_NAO_PERMITIDO"
        mensagem = "Método HTTP não permitido para este recurso."
    else:
        codigo = "REQUISICAO_INVALIDA"
        mensagem = "Não foi possível processar a requisição."

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "erro": {
                "codigo": codigo,
                "mensagem": mensagem,
                "detalhes": [],
            }
        },
    )




@app.exception_handler(Exception)
async def erro_interno(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "erro": {
                "codigo": "ERRO_INTERNO",
                "mensagem": "Ocorreu um erro interno ao processar a requisição.",
                "detalhes": [],
            }
        },
    )
