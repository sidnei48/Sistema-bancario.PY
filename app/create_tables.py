from app.database import engine, base
from app.models.models import ContaModel, TransacaoModel, ClienteModel

print("Criando tabelas...")
base.metadata.create_all(bind=engine)
print("Tabelas criadas com sucesso!")
