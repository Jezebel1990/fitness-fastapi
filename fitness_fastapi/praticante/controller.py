from fastapi import APIRouter, status, Body, HTTPException
from uuid import uuid4
from datetime import datetime
from pydantic import UUID4
from sqlalchemy import select

from fitness_fastapi.praticante.schemas import PraticanteIn, PraticanteOut, PraticanteUpdate
from fitness_fastapi.praticante.models import PraticanteModel
from fitness_fastapi.categorias.models import CategoriaModel
from fitness_fastapi.centro_treinamento.models import CentroTreinamentoModel
from fitness_fastapi.contrib.dependencies import DatabaseDependency

router = APIRouter()

@router.post(
    path="/",
    summary="Criar um novo praticante",
    status_code=status.HTTP_201_CREATED,
    response_model=PraticanteOut
)
async def post(
    db_session: DatabaseDependency,
    praticante_in: PraticanteIn = Body(...)
):
    categoria_nome = praticante_in.categoria.nome
    centro_treinamento_nome = praticante_in.centro_treinamento.nome

    categoria = (
        await db_session.execute(
            select(CategoriaModel).filter_by(nome=categoria_nome)
        )
    ).scalars().first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'A categoria {categoria_nome} não foi encontrada.'
        )

    centro_treinamento = (
        await db_session.execute(
            select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome)
        )
    ).scalars().first()

    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'O centro de treinamento {centro_treinamento_nome} não foi encontrado.'
        )

    try:
        praticante_out = PraticanteOut(
            id=uuid4(),
            created_at=datetime.utcnow(),
            **praticante_in.model_dump()
        )

        praticante_model = PraticanteModel(
            **praticante_out.model_dump(exclude={'categoria', 'centro_treinamento'})
        )

        praticante_model.categoria_id = categoria.pk_id
        praticante_model.centro_treinamento_id = centro_treinamento.pk_id

        db_session.add(praticante_model)
        await db_session.commit()

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ocorreu um erro ao inserir os dados no banco'
        )

    return praticante_out


@router.get(
    '/',
    summary='Consultar todos os Praticantes',
    status_code=status.HTTP_200_OK,
    response_model=list[PraticanteOut]
)
async def query(db_session: DatabaseDependency) -> list[PraticanteOut]:
    praticantes = (
        await db_session.execute(select(PraticanteModel))
    ).scalars().all()

    return [PraticanteOut.model_validate(praticante) for praticante in praticantes]


@router.get(
    '/{id}',
    summary='Consulta um Praticante pelo id',
    status_code=status.HTTP_200_OK,
    response_model=PraticanteOut
)
async def get(id: UUID4, db_session: DatabaseDependency) -> PraticanteOut:
    praticante = (
        await db_session.execute(
            select(PraticanteModel).filter_by(id=id)
        )
    ).scalars().first()

    if not praticante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Praticante não encontrado no id: {id}'
        )

    return praticante


@router.patch(
    '/{id}',
    summary='Editar um Praticante pelo id',
    status_code=status.HTTP_200_OK,
    response_model=PraticanteOut
)
async def patch(
    id: UUID4,
    db_session: DatabaseDependency,
    praticante_up: PraticanteUpdate = Body(...)
) -> PraticanteOut:
    praticante = (
        await db_session.execute(
            select(PraticanteModel).filter_by(id=id)
        )
    ).scalars().first()

    if not praticante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Praticante não encontrado no id: {id}'
        )

    praticante_update = praticante_up.model_dump(exclude_unset=True)

    for key, value in praticante_update.items():
        setattr(praticante, key, value)

    await db_session.commit()
    await db_session.refresh(praticante)

    return praticante


@router.delete(
    '/{id}',
    summary='Deletar um Praticante pelo id',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete(id: UUID4, db_session: DatabaseDependency) -> None:
    praticante = (
        await db_session.execute(
            select(PraticanteModel).filter_by(id=id)
        )
    ).scalars().first()

    if not praticante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Praticante não encontrado no id: {id}'
        )

    await db_session.delete(praticante)
    await db_session.commit()
