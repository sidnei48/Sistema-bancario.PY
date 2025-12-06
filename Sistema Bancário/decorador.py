from datetime import datetime
from functools import wraps

valor: float = 0.0
saldo: float = 0.0
logs = []
ARQUIVO_LOGS = "logs.txt"


# Registro
def registro(func):
    @wraps(func)
    def acao(*args, **kwargs):
        agora = datetime.now().strftime("%d/%m/%y %H:%M:%S")
        usuario = None

        # identifica o usuario
        if args and isinstance(args[0], dict):
            usuario = args[0].get("nome") or args[0].get("cpf", "")

        # monta a mensagem de log
        log_msg = f"{agora} | {func.__name__}"
        if usuario:
            log_msg += f" | usuario: {usuario}"

        # salva o log
        logs.append(log_msg)  # registra o log da ação
        with open("logs.txt", "a", encoding="utf-8") as arquivo:
            arquivo.write(log_msg + "\n")

        # executa a função original
        return func(*args, **kwargs)

    return acao


# Registro de Ação
def registrar_ação(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        resultado = func(*args, **kwargs)
        usuario = args[0]
        valor = kwargs.get("valor")
        if "valor" in kwargs:
            valor = kwargs["valor"]
        elif len(args) > 1:
            valor = args[1]
        else:
            valor = 0.0

        agora = datetime.now().strftime("%d/%m/%y %H:%M:%S")
        log_msg = f"{agora} | {func.__name__} | usuario: {usuario.titular} | valor: R$ {valor:.2f}"
        logs.append(log_msg)
        with open(ARQUIVO_LOGS, "a", encoding="utf-8") as arquivo:
            arquivo.write(log_msg + "\n")
        return resultado

    return wrapper
