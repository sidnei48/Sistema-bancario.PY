from classes import Banco
from funcoes import mostrar_logs

banco = Banco("Banco teste")
banco.carregar_contas()

print("Bem vindo ao nosso Banco!")
while True:

    # Cadastro de usuario

    cadastro = input("Voce ja possui uma conta? (s/n): ").lower()

    if cadastro == "n":
        banco.criar_conta()

    # Busca de usuario

    elif cadastro == "s":
        usuario = banco.buscar_conta_por_CPF()

        if usuario is None:
            print("Conta não encontrada.")
            print("Tente novamente ou cadastre-se. \n")
            continue
        else:
            print(f"Bem vindo, {usuario.titular}")
    else:
        print("Opção inválida.")
        continue

    executando = True
    while executando:

        # Menu
        print("\n-------- Menu --------")
        print("Escolha a operacao que deseja realizar:")
        print("1 - Depositar")
        print("2 - Sacar")
        print("3 - Extrato")
        print("4 - Logs")
        print("5 - Sair")
        print("----------------------")
        operacao = input("Digite o numero da operacao desejada: ")

        # Deposito

        if operacao == "1":
            valor = float(input("Digite o valor que deseja depositar: "))
            usuario.depositar(valor)

        # Saque

        elif operacao == "2":
            valor = float(input("Digite o valor que deseja sacar: "))
            usuario.sacar(valor)

        # Extrato

        elif operacao == "3":
            usuario.consultar_extrato()

        # logs

        elif operacao == "4":
            mostrar_logs()

        # Sair

        elif operacao == "5":
            break
        else:
            print("Operacao invalida. Por favor, escolha uma operacao valida.")
