from typing import Union

from pydantic import BaseModel


class Transacoes(BaseModel):
    tipo: str
    descricao: str
    valor: int

# class Transacoes_completa(BaseModel):
#     cliente_id: int
#     data: datetime
#     tipo: str
#     descricao: str
#     valor: int
