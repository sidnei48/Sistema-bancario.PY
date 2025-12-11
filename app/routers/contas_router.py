from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import ClienteModel, ContaModel, TransacaoModel
from app.schemas.schemas import ContaCreate, OperacaoValor, ContaResponse

router = APIRouter(prefix="/conta", tags=["Conta"])


# Criar nova conta + cliente
@router.post("/criar", response_model=ContaResponse)
def criar_conta(dados: ContaCreate, db: Session = Depends(get_db)):
    # Verifica se CPF já existe
    cliente_existente = (
        db.query(ClienteModel).filter(ClienteModel.cpf == dados.CPF).first()
    )
    if cliente_existente:
        raise HTTPException(status_code=400, detail="CPF já cadastrado.")

    # Criando cliente
    novo_cliente = ClienteModel(
        nome=dados.titular,
        cpf=dados.CPF,
        nascimento=dados.data_de_nascimento,
        estado=dados.estado,
    )
    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)

    # Criando conta
    nova_conta = ContaModel(cliente_id=novo_cliente.id, saldo=0)
    db.add(nova_conta)
    db.commit()
    db.refresh(nova_conta)

    return ContaResponse(
        id=nova_conta.id,
        titular=novo_cliente.nome,
        CPF=novo_cliente.cpf,
        data_de_nascimento=str(novo_cliente.nascimento),
        saldo=nova_conta.saldo,
    )


# Buscar conta pelo CPF
@router.get("/buscar", response_model=ContaResponse)
def buscar_conta(CPF: str, db: Session = Depends(get_db)):
    cliente = db.query(ClienteModel).filter(ClienteModel.cpf == CPF).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")

    conta = db.query(ContaModel).filter(ContaModel.cliente_id == cliente.id).first()

    return ContaResponse(
        id=conta.id,
        titular=cliente.nome,
        CPF=cliente.cpf,
        data_de_nascimento=str(cliente.nascimento),
        saldo=conta.saldo,
    )


# Listar todas as contas
@router.get("/todas")
def listar_contas(db: Session = Depends(get_db)):
    contas = db.query(ContaModel).all()
    lista = []

    for conta in contas:
        cliente = (
            db.query(ClienteModel).filter(ClienteModel.id == conta.cliente_id).first()
        )

        lista.append(
            {
                "id": conta.id,
                "titular": cliente.nome,
                "CPF": cliente.cpf,
                "estado": cliente.estado,
                "data_de_nascimento": str(cliente.nascimento),
                "saldo": conta.saldo,
            }
        )

    return {"contas": lista}


# Depositar
@router.post("/depositar")
def depositar(CPF: str, operacao: OperacaoValor, db: Session = Depends(get_db)):
    cliente = db.query(ClienteModel).filter(ClienteModel.cpf == CPF).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")

    conta = db.query(ContaModel).filter(ContaModel.cliente_id == cliente.id).first()
    conta.saldo += operacao.valor

    # cria transação
    transacao = TransacaoModel(tipo="deposito", valor=operacao.valor, conta_id=conta.id)
    db.add(transacao)
    db.commit()

    return {"mensagem": "Depósito realizado.", "saldo_atual": conta.saldo}


# Sacar
@router.post("/sacar")
def sacar(CPF: str, operacao: OperacaoValor, db: Session = Depends(get_db)):
    cliente = db.query(ClienteModel).filter(ClienteModel.cpf == CPF).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")

    conta = db.query(ContaModel).filter(ContaModel.cliente_id == cliente.id).first()

    if conta.saldo < operacao.valor:
        raise HTTPException(status_code=400, detail="Saldo insuficiente.")

    conta.saldo -= operacao.valor

    transacao = TransacaoModel(tipo="saque", valor=operacao.valor, conta_id=conta.id)
    db.add(transacao)
    db.commit()

    return {"mensagem": "Saque realizado.", "saldo_atual": conta.saldo}


# Extrato
@router.get("/extrato")
def extrato(CPF: str, db: Session = Depends(get_db)):
    cliente = db.query(ClienteModel).filter(ClienteModel.cpf == CPF).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")

    conta = db.query(ContaModel).filter(ContaModel.cliente_id == cliente.id).first()

    transacoes = (
        db.query(TransacaoModel).filter(TransacaoModel.conta_id == conta.id).all()
    )

    lista = [{"tipo": t.tipo, "valor": t.valor, "data": t.data} for t in transacoes]

    return {"extrato": lista}
