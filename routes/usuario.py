from fastapi import APIRouter, HTTPException
from models import usuario as model
from schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioLogin, Token
from sqlalchemy.orm import Session
from fastapi import Depends
from database import get_db
from typing import List
from utils.auth import hash_senha, criar_token, verificar_senha, get_current_user

router_user = APIRouter()

ADMIN_EMAIL = "oncelottti.mkt@gmail.com"  # 👈 COLOQUE SEU EMAIL

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


@router_user.get("/users")
def listar_usuarios(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Lista todos os usuários registrados.
    Apenas o admin pode acessar.
    """
    
    # Verifica se é admin
    if current_user != ADMIN_EMAIL:
        raise HTTPException(
            status_code=403,
            detail="Acesso negado. Apenas administrador pode acessar."
        )
    
    # Busca todos os usuários
    usuarios = db.query(model.Usuario).all()
    
    # Retorna os dados formatados
    return [
        {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "cpf_cnpj": usuario.cpf_cnpj,
            "data_criacao": usuario.criado_em.isoformat() if usuario.criado_em else None
        }
        for usuario in usuarios
    ]


@router_user.delete("/users/{user_id}")
def deletar_usuario(
    user_id: int,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Deleta um usuário.
    Apenas o admin pode acessar.
    """
    
    # Verifica se é admin
    if current_user != ADMIN_EMAIL:
        raise HTTPException(
            status_code=403,
            detail="Acesso negado. Apenas administrador pode deletar usuários."
        )
    
    # Busca o usuário
    usuario = db.query(model.Usuario).filter(model.Usuario.id == user_id).first()
    
    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )
    
    # Deleta o usuário
    db.delete(usuario)
    db.commit()
    
    return {"mensagem": f"Usuário {usuario.nome} deletado com sucesso"}