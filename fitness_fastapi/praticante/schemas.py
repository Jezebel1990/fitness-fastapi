from typing import Annotated, Optional
from pydantic import BaseModel, Field
from fitness_fastapi.categorias.schemas import CategoriaIn
from fitness_fastapi.centro_treinamento.schemas import CentroTreinamentoPraticante
from fitness_fastapi.contrib.schemas import BaseSchema, OutMixin


class Praticante(BaseModel):
    nome: Annotated[str, Field(description="Nome do praticante", example="João", max_length=50)]
    cpf: Annotated[str, Field(description="CPF do praticante", example="12345678900", max_length=11)]
    idade: Annotated[int, Field(description="Idade do praticante", example=30)]
    peso: Annotated[float, Field(description="Peso do praticante em kg", example=70.5)]
    altura: Annotated[float, Field(description="Altura do praticante em metros", example=1.75)]
    sexo: Annotated[str, Field(description="Sexo do praticante", example="M", max_length=1)]
    categoria: Annotated[CategoriaIn, Field(description="Categoria do praticante")]
    centro_treinamento: Annotated[
        CentroTreinamentoPraticante, 
        Field(description="Centro de treinamento do praticante")
    ]


class PraticanteIn(Praticante):
    pass


class PraticanteOut(Praticante, OutMixin):
    pass


class PraticanteUpdate(BaseSchema):
    nome: Annotated[
        Optional[str],
        Field(None, description="Nome do praticante", example="João", max_length=50)
    ]
    idade: Annotated[
        Optional[int],
        Field(None, description="Idade do praticante", example=25)
    ]
