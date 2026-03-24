from fastapi import FastAPI
from database import engine, Base
from routes.cliente import router_cliente
from routes.usuario import router_user
from fastapi.middleware.cors import CORSMiddleware

import models.cliente 
import models.usuario

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(router_cliente)
app.include_router(router_user)
