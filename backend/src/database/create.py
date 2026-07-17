import sys
from models.database import Base, engine
# Importamos os modelos explicitamente para que o metadata do SQLAlchemy os reconheça
import models.reservation

def create_database():
    """Cria todas as tabelas registradas no metadata do Base no banco de dados."""
    print("Criando tabelas no banco de dados...")
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso!")

def drop_database():
    """Remove todas as tabelas registradas no metadata do Base do banco de dados."""
    print("Removendo todas as tabelas do banco de dados...")
    Base.metadata.drop_all(bind=engine)
    print("Tabelas removidas com sucesso!")

if __name__ == "__main__":
    """ Permite execução direta via terminal para gerenciamento do banco. """
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if command == "drop":
            drop_database()
        elif command == "reset":
            drop_database()
            create_database()
        else:
            print(f"Comando desconhecido: {sys.argv[1]}. Use 'drop' ou 'reset'.")
    else:
        create_database()
