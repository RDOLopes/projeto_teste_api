from fastapi import HTTPException
from starlette import status

from app.collections.usuario import collection_usuario
from app.routers.dtos.usuario_dto import UsuarioLoginDto
from app.tools import busca_por_id, retorna_erro_operacao
from app.util import get_router, AuthHandler

autenticador = AuthHandler()
router = get_router("/auth", ["Auth"])


@router.post('/login')
def login(usuario: UsuarioLoginDto):
    try:
        user = busca_por_id(usuario.id, collection_usuario)
    except:
        raise HTTPException(status_code=401, detail="Usuario nao encontrado.")
    if user and autenticador.verificar_senha(usuario.senha, user["senha"]):
        return {'token': autenticador.encode_token(user["email"])}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Usuario ou Senha invalidos')


@router.put("/changePass/{email}/{password}/{confirm_password}")
async def alterar_senha(email: str, password: str, confirm_password: str):
    try:

        usuario = collection_usuario.find_one({"email": email})

        if not usuario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario não encontrado.")
        elif password != confirm_password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Senha e confirmar senha não correspondem")

        collection_usuario.update_one({"email": email}, {"$set": {"senha": autenticador.encriptar_senha(password)}})
        return {"Status": status.HTTP_200_OK, "Mensagem": "Senha atualizada"}

    except Exception:
        retorna_erro_operacao()