import os

SECRET = os.environ.get('JWT_SECRET','I2VzdHVkYW1haXMjZENCd2RrWVcxaGFYTXRZWEJwQ2c9PQo')
ALGORITHM = os.environ.get('JWT_ALGORITHM', 'HS256')
EXPIRE_TIME = os.environ.get('JWT_EXPIRE_TIME', 60)

ERRO_OPERACAO = "Ocorreu um erro ao realizar a operação."
SUCESSO_OPERACAO = "Operação realizada com sucesso"

TAMANHO_CODIGO = 6

DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_PORT = os.environ.get('DB_PORT')
DB_PROTOCOL = os.environ.get('DB_PROTOCOL')
DB_USER = os.environ.get('DB_USER')