from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Float,
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime, timezone

# Troca do caminho do banco SQLite
DATABASE_URL = "sqlite:///C:/Users/faria/OneDrive/Anexos/Studio visual/Estudos/Sistema Bancário/Banco.db"


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

base = declarative_base()


class ClienteModel(base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    nascimento = Column(DateTime)
    cpf = Column(String(11), unique=True, nullable=False, index=True)
    estado = Column(String(2), nullable=False)

    contas_cliente = relationship("ContaModel", back_populates="cliente_relacionado")


class ContaModel(base):
    __tablename__ = "contas"

    id = Column(Integer, primary_key=True, index=True)
    saldo = Column(Float, default=0)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)

    cliente_relacionado = relationship("ClienteModel", back_populates="contas_cliente")
    transacao_conta = relationship("TransacaoModel", back_populates="conta_relacionada")


class TransacaoModel(base):
    __tablename__ = "transacoes"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(20), nullable=False)  # 'deposito' ou 'saque'
    valor = Column(Float, nullable=False)
    data = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    conta_id = Column(Integer, ForeignKey("contas.id"), nullable=False)

    conta_relacionada = relationship("ContaModel", back_populates="transacao_conta")
