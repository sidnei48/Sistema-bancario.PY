from abc import ABC, abstractmethod
from datetime import datetime
from decorador import registro, registrar_ação


class Banco:
    def __init__(self, nome):
        self.nome = nome
        self.contas = []

    @registro
    def criar_conta(self):
        print("\n=== Criar nova conta ===")
        titular = input("Nome do titular: ")
        CPF = input("CPF do titular: ")
        data_de_nascimento = input("Data de nascimento (DD/MM/AAAA): ")
        estado = input("Qual estado você mora: ")

        for conta in self.contas:
            if conta.CPF == CPF:
                print("Essa conta ja existe!")
                exit()

        # Conversão da data de nascimento

        data_de_nascimento = datetime.strptime(data_de_nascimento, "%d/%m/%Y")
        hoje = datetime.now()

        idade = hoje.year - data_de_nascimento.year

        if idade >= 18:
            print("Bem-Vindo ao Banco Teste")
        else:
            print(f"Idade: {idade} anos - NÂO pode criar a conta.")
        nova_conta = ContaCorrente(titular, CPF, data_de_nascimento, estado, saldo=0)

        self.adicionar_conta(nova_conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)
        self.salvar_contas(conta)

    def salvar_contas(self, conta):
        with open("contas.txt", "a") as arquivo:
            arquivo.write(
                f"Titular: {conta.titular}, CPF: {conta.CPF}, Estado: {conta.estado}, Data de nascimento: {conta.data_de_nascimento}, Saldo: R${conta.saldo}\n"
            )

    def listar_contas(self):
        for conta in self.contas:
            print(conta.titular)

    def carregar_contas(self):
        try:
            with open("contas.txt", "r") as arquivo:
                for linha in arquivo:
                    dados = linha.strip().split(", ")

                    titular = dados[0].split(": ")[1]
                    CPF = dados[1].split(": ")[1]
                    estado = dados[2].split(": ")[1]
                    data_nascimento = dados[3].split(": ")[1]
                    saldo = float(dados[4].split("R$")[1])

                    data_nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d %H:%M:%S")

                    conta = ContaCorrente(titular, CPF, data_nascimento, estado, saldo)
                    self.contas.append(conta)

        except FileNotFoundError:
            pass

    @registro
    def buscar_conta_por_CPF(self):
        CPF_digitado = input("Digite o CPF: ")

        for conta in self.contas:
            if conta.CPF == CPF_digitado:
                return conta

        return None


class ContaBase(ABC):

    def __init__(self, titular, CPF, data_de_nascimento, estado, saldo=0, historico=[]):
        self.titular = titular
        self.CPF = CPF
        self.data_de_nascimento = data_de_nascimento
        self.estado = estado
        self.saldo = saldo
        self.historico = historico

    @abstractmethod
    def depositar(self, valor):
        pass

    @abstractmethod
    def sacar(self, valor):
        pass

    @abstractmethod
    def consultar_extrato(self, valor):
        pass


class ContaCorrente(ContaBase):

    @registrar_ação
    def depositar(self, valor_deposito):
        if valor_deposito > 0:
            self.saldo += valor_deposito
            self.historico.append(f"Depósito: +R${valor_deposito} | Saldo: R${self.saldo}")
            with open("contas.txt", "r") as arquivo:
                linhas = arquivo.readlines()

            linhas_novas = []
            for linha in linhas:
                if f"CPF: {self.CPF}" in linha:
                    nova_linha = (
                        f"Titular: {self.titular}, CPF: {self.CPF}, Estado: {self.estado}, "
                        f"Data de nascimento: {self.data_de_nascimento}, Saldo: R${self.saldo}\n"
                    )
                    linhas_novas.append(nova_linha)
                else:
                    linhas_novas.append(linha)

            with open("contas.txt", "w") as arquivo:
                arquivo.writelines(linhas_novas)
            print(f"Deposito realizado com sucesso! Saldo atual: R${self.saldo}")

        else:
            print("Valor invalido. O valor do deposito deve ser maior que zero.")

    @registrar_ação
    def sacar(self, valor_sacado):
        if valor_sacado > 0:
            self.saldo -= valor_sacado
            self.historico.append(f"Saque: -R${valor_sacado} | Saldo: R${self.saldo}")
            with open("contas.txt", "r") as arquivo:
                linhas = arquivo.readlines()

            linhas_novas = []
            for linha in linhas:
                if f"CPF: {self.CPF}" in linha:
                    nova_linha = (
                        f"Titular: {self.titular}, CPF: {self.CPF}, Estado: {self.estado}, "
                        f"Data de nascimento: {self.data_de_nascimento}, Saldo: R${self.saldo}\n"
                    )
                    linhas_novas.append(nova_linha)
                else:
                    linhas_novas.append(linha)

            with open("contas.txt", "w") as arquivo:
                arquivo.writelines(linhas_novas)
            print(f"Saque realizado com sucesso! Saldo atual: R${self.saldo}")

        else:
            print("Valor invalido. O valor do saque deve ser maior que zero.")

    @registrar_ação
    def consultar_extrato(self):
        print("\n====Extrato====")
        if len(self.historico) == 0:
            print("Nenhuma Movimentação.")
        else:
            for mov in self.historico:
                print(mov)
        print("====Fim do Extrato====\n")

