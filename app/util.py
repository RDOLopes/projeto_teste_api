import jwt

from fastapi import HTTPException, Security, APIRouter
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from passlib.context import CryptContext
from datetime import datetime, timedelta

from settings import SECRET, EXPIRE_TIME, ALGORITHM


def get_router(prefix, tags):
    return APIRouter(
        prefix=prefix,
        tags=tags,
        responses={404: {"description": "Not found"}},
    )


class AuthHandler():
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = SECRET

    def encriptar_senha(self, password):
        return self.pwd_context.hash(password)

    def verificar_senha(self, plain_password, password_encriptado):
        return self.pwd_context.verify(plain_password, password_encriptado)

    def encode_token(self, user_id):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, minutes=int(EXPIRE_TIME)),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm=ALGORITHM
        )

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=[ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Token vencido, por favor efetuar login.')
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail='Token invalido.')

    def auth_wrapper(self, autenticar: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(autenticar.credentials)
