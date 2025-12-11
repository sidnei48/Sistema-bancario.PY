from .decorador import logs
import csv


# Mostra logs (com ou sem filtro)
def mostrar_logs(filtro=None):
    print("\n==== Logs encontrados ====")
    encontrou = False

    for log in filtrar_logs(filtro):
        print(log)
        encontrou = True

    if not encontrou:
        print("Nenhum log encontrado.")


# Filtra logs por ação (ou retorna todos se filtro=None)
def filtrar_logs(acao=None):
    for log in logs:
        if acao is None or acao.lower() in log.lower():
            yield log


def criar_conta_api(self, nome, cpf):
    conta = self.buscar_conta_por_CPF(cpf)
    if conta:
        return {"erro": "Conta já existe"}

    nova = self.criar_conta(nome=nome, cpf=cpf)
    return {"mensagem": "Conta criada com sucesso", "titular": nome, "cpf": cpf}


def buscar_conta_por_cpf_api(self, cpf):
    conta = self.buscar_conta_por_CPF(cpf)
    if not conta:
        return None
    return {"titular": conta.titular, "cpf": conta.cpf, "saldo": conta.saldo}
