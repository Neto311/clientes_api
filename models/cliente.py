from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database import Base
from datetime import datetime


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String)
    cpf = Column(String)
    usuario_id = Column(Integer, ForeignKey("usuario.id"))  # ← Vinculo com usuário
    criado_em = Column(DateTime, default=datetime.now)