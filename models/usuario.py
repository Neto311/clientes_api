from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class Usuario (Base):
    __tablename__ = "usuario"

    id = Column (Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String, unique=True)
    cpf_cnpj = Column(String)
    criado_em = Column(DateTime, default=datetime.now)
    senha_hash = Column(String)
