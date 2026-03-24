from pydantic import BaseModel, ConfigDict, Field, field_validator, EmailStr

class ClienteCreate(BaseModel):
    nome: str = Field(min_length=3)
    email: EmailStr 
    cpf: str = Field (min_length=11, max_length=14, )

    @field_validator('email')
    def validar_email(cls,v):
        if '@' not in v:
            raise ValueError ("email inválido")
        return v
    
    @field_validator('nome')
    @classmethod
    def validar_nome(cls, valor):
        return valor.title()
    
    @field_validator('cpf')
    def validar_cpf(cls, valor):
        cpf_limpo = valor.replace(".","").replace("-","")
        if len (cpf_limpo) != 11:
            raise ValueError ("CPF deve conter 11 números")
        
        if not cpf_limpo.isdigit():
            raise ValueError ("CPF deve conter apenas números")
        
        cpf_formatado = f"{cpf_limpo[0:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:11]}"
        return cpf_formatado


class ClienteResponse(BaseModel):
    id: int
    nome: str
    email: str
    cpf: str

    model_config = ConfigDict(from_attributes=True)