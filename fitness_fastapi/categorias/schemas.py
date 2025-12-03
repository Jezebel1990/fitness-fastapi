from typing import Annotated

from pydantic import Field, UUID4
from fitness_fastapi.contrib.schemas import BaseSchema

class CategoriaIn(BaseSchema):
    nome: Annotated[str, Field(description='Nome da categoria', example='Musculação', max_length=20)]


class CategoriaOut(CategoriaIn):
    id: Annotated[UUID4, Field(description='Identificador da categoria')]