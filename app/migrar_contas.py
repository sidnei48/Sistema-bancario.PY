import datetime
from .models.models import ClienteModel, ContaModel
from .database import SessionLocal

db = SessionLocal()
arquivo_txt = "contas.txt"

with open(arquivo_txt, "r", encoding="utf-8") as arquivo:
    for linha in arquivo:
        linha = linha.strip()
        if not linha:
            continue

        partes = linha.split(", ")
        dados = {parte.split(": ", 1)[0].strip(): parte.split(": ", 1)[1].strip() for parte in partes}

        nome = dados["Titular"]
        cpf = dados["CPF"]
        estado = dados["Estado"]
        nascimento = datetime.datetime.strptime(dados["Data de nascimento"], "%Y-%m-%d %H:%M:%S")
        saldo = float(dados["Saldo"].replace("R$", "").replace(",", "."))

        # Verifica se já existe cliente com este CPF
        cliente_existente = db.query(ClienteModel).filter_by(cpf=cpf).first()

        if cliente_existente:
            # Já existe, não adiciona
            continue

        # Adiciona novo cliente
        novo_cliente = ClienteModel(
            nome=nome,
            cpf=cpf,
            estado=estado,
            nascimento=nascimento
        )
        db.add(novo_cliente)
        db.commit()

        # Adiciona conta
        nova_conta = ContaModel(
            saldo=saldo,
            cliente_id=novo_cliente.id
        )
        db.add(nova_conta)
        db.commit()

print("Migração concluída! Apenas novos clientes foram adicionados.")
db.close()
