from typing import List

from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import exc
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from app.routers.dtos.noticia_dto import NoticiaDto
from app.tables.noticia import Noticia
from app.settings import ERRO_OPERACAO, SUCESSO_OPERACAO
from app.util import AuthHandler, get_router, get_db

router = get_router("/noticias", ["Noticia"])
autenticador = AuthHandler()


def verificar_existencia_noticia(noticia):
    if noticia is not None:
        return True
    return False


def retorna_erro_noticia_nao_encontrada(id_noticia):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"A notícia de id {id_noticia} não foi encontrada")


@router.get("/")
async def buscar_todas(
        db: Session = Depends(get_db),
        token=Depends(autenticador.auth_wrapper)
) -> List[NoticiaDto]:
    try:
        noticias = db.query(Noticia).all()
        if noticias:
            dados = [NoticiaDto(noticia.titulo, noticia.conteudo, noticia.data_publicacao) for noticia in noticias]
            return JSONResponse(status_code=status.HTTP_200_OK, content={"mensagem": SUCESSO_OPERACAO, "dados": jsonable_encoder(dados)})
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhuma notícia encontrada.")
    except exc.SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ERRO_OPERACAO)


@router.post("/")
async def criar(noticia_dto: NoticiaDto, token=Depends(autenticador.auth_wrapper), db: Session = Depends(get_db)) -> NoticiaDto:
    try:
        noticia = Noticia(titulo=noticia_dto.titulo,
                          conteudo=noticia_dto.conteudo,
                          data_publicacao=noticia_dto.data_publicacao)

        db.add(noticia)
        db.commit()
        db.refresh(noticia)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"mensagem": SUCESSO_OPERACAO, "dados": jsonable_encoder(noticia_dto)})

    except exc.SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ERRO_OPERACAO)


@router.put("/")
async def alterar(noticia_dto: NoticiaDto, token=Depends(autenticador.auth_wrapper), db: Session = Depends(get_db)) -> NoticiaDto:
    try:
        noticia = db.query(Noticia).filter(Noticia.id == noticia_dto.id).first()
        if verificar_existencia_noticia(noticia):
            noticia.titulo = noticia_dto.titulo
            noticia.conteudo = noticia_dto.conteudo
            noticia.data_publicacao = noticia_dto.data_publicacao
            db.commit()
            db.refresh(noticia)
            return JSONResponse(status_code=status.HTTP_200_OK, content={"mensagem": SUCESSO_OPERACAO, "dados": jsonable_encoder(noticia_dto)})
        retorna_erro_noticia_nao_encontrada(noticia_dto.id)

    except exc.SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ERRO_OPERACAO)


@router.delete("/")
async def delete(noticia_id: int, token=Depends(autenticador.auth_wrapper), db: Session = Depends(get_db)):
    try:
        noticia = db.query(Noticia).filter(Noticia.id == noticia_id)
        if verificar_existencia_noticia(noticia.first()):
            db.query(Noticia).filter(Noticia.Id == noticia_id).delete()
            db.commit()
            return JSONResponse(status_code=status.HTTP_200_OK, content={"mensagem": SUCESSO_OPERACAO})
        retorna_erro_noticia_nao_encontrada(noticia.id)
    except exc.SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ERRO_OPERACAO)


