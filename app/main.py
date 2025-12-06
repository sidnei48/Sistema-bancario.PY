from fastapi import FastAPI
from Sistema.classes import Banco
from Sistema.funcoes import mostrar_logs

app = FastAPI(title="API do Sistema de Banco")

# Inicialização do banco
banco = Banco("project bank")
banco.carregar_contas()


@app.get("/")
def home():
    return {"message": "Bem vindo ao nosso Banco!"}


@app.post("/conta/criar")
def criar_conta(titular: str, CPF: int, data_de_nascimento: str, estado: str):
    conta = banco.criar_conta(titular, CPF, data_de_nascimento, estado)
    return conta


@app.get("/conta/buscar")
def buscar_conta(CPF: int):
    conta = banco.buscar_conta_por_CPF_api(CPF)
    return conta


@app.get("/contas")
def listar_contas():
    lista_formatada = []

    for conta in banco.contas:
        lista_formatada.append(
            {
                "titular": conta.titular,
                "cpf": conta.CPF,
                "estado": conta.estado,
                "data_de_nascimento": conta.data_de_nascimento.strftime("%d/%m/%Y"),
            }
        )

    return {"contas": lista_formatada}

@app.post("/conta/depositar")
def depositar(CPF: int, valor: float):
    conta = banco.buscar_conta_por_CPF_api(CPF)

    if not conta:
        return {"error": "Conta não encontrada."}

    conta.depositar(valor)
    return {
        "message": f"Depósito de R${valor} realizado com sucesso, saldo atual: R${conta.saldo}"
    }


@app.post("/conta/sacar")
def sacar(CPF: int, valor: float):
    conta = banco.buscar_conta_por_CPF_api(CPF)

    if not conta:
        return {"error": "Conta não encontrada."}

    ok = conta.sacar(valor)
    if not ok:
        return {"error": "Saldo insuficiente."}

    return {
        "message": f"Saque de R${valor} realizado com sucesso, saldo atual: R${conta.saldo}"
    }


@app.get("/conta/extrato")
def consultar_extrato(CPF: int):
    conta = banco.buscar_conta_por_CPF_api(CPF)

    if not conta:
        return {"error": "Conta não encontrada."}

    return {"extrato": conta.consultar_extrato()}


@app.get("/logs")
def get_logs():
    return {"logs": mostrar_logs()}
