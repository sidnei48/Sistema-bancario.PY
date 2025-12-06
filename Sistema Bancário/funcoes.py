from decorador import logs
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
