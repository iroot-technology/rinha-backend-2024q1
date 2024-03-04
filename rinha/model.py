from typing import Union

from pydantic import BaseModel


class Transacoes(BaseModel):
    tipo: str
    descricao: str
    valor: int

