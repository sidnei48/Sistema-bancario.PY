from fastapi import FastAPI
from app.routers.contas_router import router as contas_router

app = FastAPI(title="API do Sistema de Banco")

# Registrando as rotas
app.include_router(contas_router)

@app.get("/")
def home():
    return {"message": "Bem-vindo ao nosso Banco!"}
