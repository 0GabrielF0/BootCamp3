
from pydantic import BaseModel, ConfigDict


class PlacaEntrada(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=False)

    placa: str


class ResultadoValidacao(BaseModel):
    placa_original: str
    placa_normalizada: str
    valida: bool
    padrao: str | None
    mensagem: str
