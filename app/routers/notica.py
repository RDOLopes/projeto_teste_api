from typing import List

from fastapi import Depends, HTTPException

from starlette import status
from starlette.responses import JSONResponse

from app.routers.dtos.noticia_dto import NoticiaDto
from app.settings import SUCESSO_OPERACAO
from app.collections.noticia import collection_noticia
from app.tools import busca_por_id, verificar_existencia, retorna_erro_nao_encontrado, retorna_json_busca_id, \
    retorna_json, retorna_sucesso_operacao, retorna_erro_operacao, retorna_json_update
from app.util import AuthHandler, get_router

router = get_router("/noticias", ["Noticia"])
autenticador = AuthHandler()


def retorna_noticia_dto(noticia):
    return NoticiaDto(id=noticia["id"], titulo=noticia["titulo"], conteudo=noticia["conteudo"],data_publicacao=noticia["data_publicacao"])


@router.get("/")
async def buscar(token=Depends(autenticador.auth_wrapper)) -> List[NoticiaDto]:
    noticias = collection_noticia.find({})
    if noticias.count() > 0:
        array_noticias_dto = [retorna_noticia_dto(noticia) for noticia in noticias]
        return retorna_sucesso_operacao(array_noticias_dto)
    retorna_erro_nao_encontrado()


@router.get("/{noticia_id}")
async def buscar(noticia_id, token=Depends(autenticador.auth_wrapper)) -> List[NoticiaDto]:
    try:
        noticia = busca_por_id(noticia_id, collection_noticia)
    except Exception:
        raise retorna_erro_operacao()
    if verificar_existencia(noticia):
        return retorna_sucesso_operacao(retorna_noticia_dto(noticia))
    retorna_erro_nao_encontrado()


@router.post("/")
async def criar(noticia_dto: NoticiaDto, token=Depends(autenticador.auth_wrapper)) -> NoticiaDto:
    try:
        collection_noticia.insert_one(retorna_json(noticia_dto))
        return retorna_sucesso_operacao(noticia_dto)
    except Exception:
        retorna_erro_operacao()


@router.put("/")
async def alterar(noticia_dto: NoticiaDto, token=Depends(autenticador.auth_wrapper)) -> NoticiaDto:
    if verificar_existencia(busca_por_id(noticia_dto.id, collection_noticia)):
        try:
            collection_noticia.update_one(retorna_json_busca_id(noticia_dto.id), retorna_json_update(noticia_dto))
            return retorna_sucesso_operacao(noticia_dto)
        except Exception:
            retorna_erro_operacao()
    retorna_erro_nao_encontrado()


@router.delete("/")
async def delete(noticia_id: int, token=Depends(autenticador.auth_wrapper)):
    if verificar_existencia(busca_por_id(noticia_id, collection_noticia)):
        try:
            collection_noticia.delete_one(retorna_json_busca_id(noticia_id))
            return JSONResponse(status_code=status.HTTP_200_OK, content={"mensagem": SUCESSO_OPERACAO})
        except Exception:
            retorna_erro_operacao()
    retorna_erro_nao_encontrado()

