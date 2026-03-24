from fastapi import APIRouter, HTTPException
from models import cliente as model
from schemas.cliente import ClienteCreate, ClienteResponse
from sqlalchemy.orm import Session
from fastapi import Depends
from database import get_db
from typing import List
from utils.auth import get_current_user
from models.usuario import Usuario
from models.cliente import Cliente

router_cliente = APIRouter()

@router_cliente.post("/clientes", response_model = ClienteResponse)
def criar_cliente(
    cliente: ClienteCreate, 
    email_usuario: str = Depends(get_current_user),
    db: Session = Depends(get_db) ):

    usuario = db.query (Usuario).filter(Usuario.email == email_usuario).first()

    novo_cliente = model.Cliente(
        cpf=cliente.cpf,
        email=cliente.email,
        nome=cliente.nome,
        usuario_id = usuario.id
    )

    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)

    return novo_cliente

@router_cliente.get("/clientes", response_model=List[ClienteResponse])
def listar_clientes(
    email_usuario: str = Depends (get_current_user), 
    db: Session = Depends(get_db)):
    
    usuario = db.query(Usuario).filter (Usuario.email == email_usuario).first()
    return db.query(Cliente).filter(Cliente.usuario_id == usuario.id).all()


@router_cliente.get("/clientes/{id}", response_model=ClienteResponse)
def buscar_cliente(
    id: int, 
    email_usuario: str = Depends(get_current_user),
    db: Session = Depends(get_db)):

    usuario = db.query(Usuario).filter (Usuario.email == email_usuario).first()

    cliente = db.query(Cliente).filter((Cliente.id == id) & (Cliente.usuario_id == usuario.id)).first()

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente


@router_cliente.put("/clientes/{id}")
def atualizar_cliente(
    id: int, 
    cliente: ClienteCreate, 
    email_usuario: str = Depends(get_current_user),
    db: Session = Depends(get_db)):

    usuario = db.query(Usuario).filter (Usuario.email == email_usuario).first()

    cliente_db = db.query(Cliente).filter((Cliente.id == id) & (Cliente.usuario_id == usuario.id)).first()

    if not cliente_db:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    cliente_db.nome = cliente.nome
    cliente_db.email = cliente.email
    cliente_db.cpf = cliente.cpf

    db.commit()
    db.refresh(cliente_db)

    return {
        "mensagem": f"Estes são os novos dados do seu cliente. Cliente: {cliente_db.nome}, CPF: {cliente_db.cpf}, Email: {cliente_db.email}"}


@router_cliente.delete("/clientes/{id}")
def deletar_cliente(
    id: int, 
    email_usuario: str = Depends(get_current_user),
    db: Session = Depends(get_db)):

    usuario = db.query(Usuario).filter (Usuario.email == email_usuario).first()

    cliente_delete_db = db.query(Cliente).filter((Cliente.usuario_id == usuario.id) & (Cliente.id == id)).first()

    if not cliente_delete_db:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    db.delete(cliente_delete_db)
    db.commit()

    return {
        "mensagem": f"Cliente: {cliente_delete_db.nome}, CPF: {cliente_delete_db.cpf}, Email: {cliente_delete_db.email} foi deletado com sucesso"
        }

