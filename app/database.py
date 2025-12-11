from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# Caminho do banco SQLite
DATABASE_URL = "sqlite:///C:/Users/faria/OneDrive/Anexos/Studio visual/Estudos/Sistema Bancario/Banco.db"


# Criação o moto de conexão com o banco de dados
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Criação de classe SessionLocaç, que sera usada para abrir conexões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# classe base para os models herdarem
base = declarative_base()


# Dependência que será usada nas rotas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from app.models.models import base as ModelBase

ModelBase.metadata.create_all(bind=engine)