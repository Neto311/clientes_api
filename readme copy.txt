# API Clientes - FastAPI

Uma API REST para gerenciar clientes com autenticação JWT.

## 🚀 Funcionalidades

- ✅ Registro e Login de usuários
- ✅ Autenticação com JWT
- ✅ CRUD completo de clientes
- ✅ Hash seguro de senhas com Argon2
- ✅ Banco de dados SQLite

## 📦 Instalação

```bash
# Clone o repositório
git clone https://github.com/Neto311/clientes_api.git
cd clientes_api

# Crie um ambiente virtual
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

#Como executar
python3 -m uvicorn main:app --reload

#A API estará disponivel em:
A API estará disponível em: http://127.0.0.1:8000
Docs interativa: http://127.0.0.1:8000/docs


Endpoints
Autenticação
POST /register - Registrar novo usuário
POST /login - Fazer login (retorna token JWT)
Clientes
POST /clientes - Criar cliente
GET /clientes - Listar clientes do usuário
GET /clientes/{id} - Obter cliente específico
PUT /clientes/{id} - Atualizar cliente
DELETE /clientes/{id} - Deletar cliente

Autenticação
Todos os endpoints de clientes requerem um token JWT no header:

Code
Authorization: Bearer {token}

🛠️ Tecnologias
FastAPI
SQLAlchemy
SQLite
JWT (python-jose)
Passlib + Argon2
📝 Autor
Neto311

📄 Licença
MIT

Code

---

## 🔌 **PASSO 6: Fazer o commit inicial**

```bash
cd ~/Documents/clientes_api
git add .
git commit -m "Initial commit: API FastAPI com autenticação e CRUD de clientes"



