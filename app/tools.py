from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse

from app.collections.connection.database import mongo_database
from app.settings import SUCESSO_OPERACAO, ERRO_OPERACAO


def verificar_existencia(necessito_verificacao):
    if necessito_verificacao is not None:
        return True
    return False


def retorna_json_busca_id(id):
    return {"id": id}


def busca_por_id(id, collection):
    return collection.find_one(retorna_json_busca_id(int(id)))


def retorna_json(receber_encode_json):
    return jsonable_encoder(receber_encode_json)


def retorna_sucesso_operacao(retorno):
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"mensagem": SUCESSO_OPERACAO, "dados": retorna_json(retorno)})


def retorna_erro_operacao():
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ERRO_OPERACAO)


def retorna_erro_nao_encontrado():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum resultado foi encontrado.")


def retorna_json_update(informacao_update):
    return {"$set": retorna_json(informacao_update)}



