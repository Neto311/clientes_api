from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext


pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)


SECRET_KEY = "sdjkvnd-dshfnv-ndehj35-#fhsk " #Chave ficticia, para teste do projeto, verdadeira chave encontra-se segura
ALGORITHM = "HS256"
ACESS_TOKEN_EXPIRE_MINUTES = 30

def hash_senha (senha: str):
    return pwd_context.hash(senha)

def verificar_senha (senha: str, hash_senha: str):
    return pwd_context.verify(senha, hash_senha)
    
    
def criar_token(data: dict, expire_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy ()
    if expire_delta:
        expire = datetime.utcnow() + expire_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update ({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def validar_token (token:str):
    try:
        payload = jwt.decode (token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
    
        
security = HTTPBearer()

def get_current_user (credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = validar_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail = "Token inválido")
    
    email = payload.get("sub")
    return email

