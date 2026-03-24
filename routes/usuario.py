from fastapi import APIRouter, HTTPException
from models import usuario as model
from schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioLogin, Token
from sqlalchemy.orm import Session
from fastapi import Depends
from database import get_db
from typing import List
from utils.auth import hash_senha, criar_token, verificar_senha

router_user = APIRouter()

@router_user.post("/register", response_model = UsuarioResponse)
def registrar(usuario: UsuarioCreate, db: Session = Depends(get_db)):

    senha_hash = hash_senha(usuario.senha)

    usuario_existente = db.query(model.Usuario).filter(model.Usuario.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException (status_code=401, detail="Email já cadastrado")
   
    novo_usuario = model.Usuario(
        email=usuario.email,
        nome=usuario.nome,
        cpf_cnpj=usuario.cpf_cnpj,
        senha_hash = senha_hash
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return novo_usuario 


@router_user.post("/login", response_model= Token)
def login(usuario_login: UsuarioLogin, db: Session = Depends(get_db)):
    usuario = db.query(model.Usuario).filter (model.Usuario.email == usuario_login.email).first()

    if not usuario or not verificar_senha (usuario_login.senha, usuario.senha_hash):
        raise HTTPException (status_code=401, detail= ("Email ou senha não encontrado"))
    
    access_token = criar_token(data = {"sub": usuario.email})

    return {"access_token": access_token, "token_type":"bearer"}
