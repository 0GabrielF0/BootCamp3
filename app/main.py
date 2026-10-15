
from fastapi import FastAPI
from app.schemas import PlacaEntrada, ResultadoValidacao
from app.validator import validar_placa

app = FastAPI(
    title="Validador de Placas Brasileiras",
    description=(
        "API para validar os formatos antigo e Mercosul "
        "de placas brasileiras."
    ),
    version="1.0.0"
)


@app.get("/")
def inicio():
    return {
        "projeto": "Validador de Placas Brasileiras",
        "status": "operacional",
        "documentacao": "/docs"
    }


@app.post("/validate", response_model=ResultadoValidacao)
def validar(dados: PlacaEntrada):
    return validar_placa(dados.placa)
