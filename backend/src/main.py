import datetime
from colour import Color
from sqlalchemy.orm import Session

from database.create import create_database, drop_database
from models.database import engine
from models.reservation import UserTable, ArtifactTable
from services.reservation import (
    add_user,
    add_artifact,
    add_category,
    add_reservation,
    get_reservation
)

def main():
    print("Reiniciando banco de dados...")
    drop_database()
    create_database()

    # 1. Criar categorias
    print("Criando categorias...")
    add_category("Salas de Aula", Color("blue"))
    add_category("Laboratórios", Color("green"))

    # 2. Criar salas (artefatos)
    print("Criando salas...")
    add_artifact("Sala C16", "Sala de aula Capacidade 10 pessoas", "Salas de Aula")
    add_artifact("Lab FabTec", "Laboratório de fabricação de hardware", "Laboratórios")

    # 3. Criar usuários
    print("Criando usuários...")
    add_user("Hylson", "hylson@exemplo.com")
    add_user("André", "andre@exemplo.com")
    add_user("Gabriel", "gabriel@exemplo.com")

    # 4. Criar reserva com observadores
    print("Criando reserva com observadores...")
    add_reservation(
        user="Hylson",
        artifact="Sala C16",
        date=datetime.date.today(),
        start_time=datetime.time(13, 0),
        end_time=datetime.time(17, 0),
        purpose="Reunião de equipe para planejamento do projeto",
        observations="Trazer notebook e caneca",
        observers=["André", "Gabriel"]
    )

    # 5. Consultar reservas
    print("\n--- Consultando Reservas via Serviço ---")
    reservas = get_reservation(user="Hylson", artifact="Sala C16")

    # Usamos uma sessão apenas para buscar os nomes do criador e da sala a partir de seus IDs
    with Session(engine) as session:
        for res in reservas:
            criador = session.get(UserTable, res.user)
            sala = session.get(ArtifactTable, res.artifact)
            
            print(f"Reserva ID: {res.id}")
            print(f"  Criador: {criador.name} ({criador.email})")
            print(f"  Local/Sala: {sala.name}")
            print(f"  Data/Horário: {res.date} das {res.start_time} às {res.end_time}")
            print(f"  Objetivo: {res.purpose}")
            print(f"  Observações: {res.observations}")
            
            # Listamos os observadores (que já foram buscados ansiosamente pelo serviço)
            nomes_observadores = [obs.name for obs in res.observers]
            print(f"  Observadores Notificados: {', '.join(nomes_observadores) if nomes_observadores else 'Nenhum'}")

if __name__ == "__main__":
    main()