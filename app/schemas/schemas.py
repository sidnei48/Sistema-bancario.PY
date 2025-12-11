from pydantic import BaseModel


class ContaCreate(BaseModel):
    titular: str
    CPF: str
    data_de_nascimento: str
    estado: str  


class ContaResponse(BaseModel):
    id: int
    titular: str
    CPF: str
    data_de_nascimento: str
    saldo: float

    class Config:
        orm_mode = True


class OperacaoValor(BaseModel):
    valor: float
