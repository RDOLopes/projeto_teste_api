from typing import List

from fastapi import Depends, HTTPException

from starlette import status
from starlette.responses import JSONResponse

from app.routers.dtos.noticia_dto import NoticiaDto
from app.settings import ERRO_OPERACAO, SUCESSO_OPERACAO
from app.collections.noticia import collection_noticia
from app.tools import busca_por_id, verificar_existencia, retorna_erro_nao_encontrado, retorna_json_busca_id, \
    retorna_json, retorna_sucesso_operacao, retorna_erro_operacao
from app.util import AuthHandler, get_router

router = get_router("/noticias", ["Noticia"])
autenticador = AuthHandler()


@router.get("/")
async def buscar(token=Depends(autenticador.auth_wrapper)) -> List[NoticiaDto]:
    try:
        noticias = collection_noticia.find()
        if noticias:
            array_noticias_dto = [NoticiaDto(noticia.titulo, noticia.conteudo, noticia.data_publicacao) for noticia in
                                  noticias]
            return retorna_sucesso_operacao(array_noticias_dto)
        else:
            retorna_erro_nao_encontrado()
    except Exception:
        retorna_erro_operacao()


@router.get("/")
async def buscar(noticia_id, token=Depends(autenticador.auth_wrapper)) -> List[NoticiaDto]:
    try:
        noticia = busca_por_id(noticia_id)
        if verificar_existencia(noticia):
            return retorna_sucesso_operacao(noticia)
        retorna_erro_nao_encontrado()
    except Exception:
        raise retorna_erro_operacao()


@router.post("/")
async def criar(noticia_dto: NoticiaDto, token=Depends(autenticador.auth_wrapper)) -> NoticiaDto:
    try:
        noticia_json = retorna_json(noticia_dto)
        collection_noticia.insert_one(noticia_json)
        return retorna_sucesso_operacao(noticia_dto)
    except Exception:
        retorna_erro_operacao()


@router.put("/")
async def alterar(noticia_dto: NoticiaDto, token=Depends(autenticador.auth_wrapper)) -> NoticiaDto:
    try:
        if verificar_existencia(busca_por_id(noticia_dto.id, collection_noticia)):
            json_noticia = retorna_json(noticia_dto)
            collection_noticia.update_one(retorna_json_busca_id(noticia_dto.id), json_noticia)
            return retorna_sucesso_operacao(noticia_dto)
        retorna_erro_nao_encontrado(noticia_dto.id)
    except Exception:
        retorna_erro_operacao()


@router.delete("/")
async def delete(noticia_id: int, token=Depends(autenticador.auth_wrapper)):
    try:
        if verificar_existencia(busca_por_id(noticia_id)):
            collection_noticia.delete_one(retorna_json_busca_id(noticia_id))
            return JSONResponse(status_code=status.HTTP_200_OK, content={"mensagem": SUCESSO_OPERACAO})
        retorna_erro_nao_encontrado(noticia_id)
    except Exception:
        retorna_erro_operacao()
