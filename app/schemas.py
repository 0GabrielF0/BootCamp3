
from pydantic import BaseModel, ConfigDict


class ValidarPlacaRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=False)

    placa: str


class ValidarPlacaResponse(BaseModel):
    valida: bool
    placa_normalizada: str | None
    padrao: str | None
    motivo: str | None
    mensagem: str


class DetalheErro(BaseModel):
    campo: str
    problema: str


class CorpoErro(BaseModel):
    codigo: str
    mensagem: str
    detalhes: list[DetalheErro]


class ErroResponse(BaseModel):
    erro: CorpoErro
