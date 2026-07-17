import datetime

from colour import Color
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, selectinload

from models.reservation import UserTable, CategoryTable, ArtifactTable, ReservationTable

engine = create_engine("sqlite:///fabtec.db", echo=False)

def add_user(name: str, email: str):
    """ Adiciona um novo usuário ao banco de dados. 
    
        Args:
            name (str): Nome do usuário.
            email (str): Email do usuário.
        Returns:
            int: ID do usuário adicionado.
    """
    with Session(engine) as session:
        user = UserTable(name=name, email=email)
        session.add(user)
        session.commit()
        return user.id

def add_artifact(name: str, description: str, category_name: str):
    """ Adiciona um novo artefato associado a uma categoria. 
    
        Args:
            name (str): Nome do artefato (ex: Sala C16).
            description (str): Descrição ou especificações do artefato.
            category_name (str): Nome da categoria associada.
        Returns:
            int: ID do artefato adicionado.
    """
    with Session(engine) as session:
        category = session.execute(select(CategoryTable).where(CategoryTable.name == category_name)).scalar_one()
        artifact = ArtifactTable(name=name, description=description, category=category.id)
        session.add(artifact)
        session.commit()
        return artifact.id

def add_category(name: str, color: Color):
    """ Adiciona uma nova categoria de artefatos. 
    
        Args:
            name (str): Nome da categoria (ex: Salas de Reunião).
            color (Color): Cor representativa para a categoria.
        Returns:
            None
    """
    with Session(engine) as session:
        category = CategoryTable(name=name, color=color)
        session.add(category)
        session.commit()

def get_category(name: str = None, color: Color = None):
    """ Busca categorias com base nos filtros fornecidos. 
    
        Args:
            name (str, optional): Nome da categoria para filtrar.
            color (Color, optional): Cor da categoria para filtrar.
        Returns:
            list[CategoryTable]: Lista de categorias encontradas.
    """
    with Session(engine) as session:
        query = select(CategoryTable)
        if name:
            query = query.where(CategoryTable.name == name)
        if color:
            query = query.where(CategoryTable.color == color)
        return session.execute(query).scalars().all()

def add_reservation(
        user: str, 
        artifact: str, 
        date: datetime.date, 
        start_time: datetime.time, 
        end_time: datetime.time, 
        purpose: str, 
        observations: str = None,
        observers: list[str] = None
    ):
    """ Cria uma nova reserva, realizando validações e associando observadores. 
    
        Args:
            user (str): Nome do usuário criador.
            artifact (str): Nome do artefato (sala/equipamento).
            date (datetime.date): Data da reserva.
            start_time (datetime.time): Horário de início.
            end_time (datetime.time): Horário de término.
            purpose (str): Objetivo da reserva.
            observations (str, optional): Observações da reserva.
            observers (list[str], optional): Lista de nomes dos observadores.
        Returns:
            None
    """
    with Session(engine) as session:
        user_obj = session.execute(select(UserTable).where(UserTable.name == user)).scalar_one()
        artifact_obj = session.execute(select(ArtifactTable).where(ArtifactTable.name == artifact)).scalar_one()

        if get_reservation(user=user, artifact=artifact, date=date, start_time=start_time, end_time=end_time, active=True):
            raise ValueError("Reservation already exists for the given parameters.")
        
        reservation = ReservationTable(
            user=user_obj.id,
            artifact=artifact_obj.id,
            date=date,
            start_time=start_time,
            end_time=end_time,
            purpose=purpose,
            observations=observations,
            created_at=datetime.datetime.now()
        )

        if observers:
            for obs_name in observers:
                obs_user = session.execute(select(UserTable).where(UserTable.name == obs_name)).scalar_one()
                reservation.observers.append(obs_user)

        session.add(reservation)
        session.commit()

def get_reservation(
        user: str = None, 
        artifact: str = None, 
        date: datetime.date = None, 
        start_time: datetime.time = None, 
        end_time: datetime.time = None, 
        purpose: str = None, 
        category_name: str = None, 
        observations: str = None,
        active: bool = None
    ):
    """ Filtra e retorna as reservas cadastradas de acordo com os critérios fornecidos. 
    
        Args:
            user (str, optional): Nome do usuário criador.
            artifact (str, optional): Nome do artefato (sala/equipamento).
            date (datetime.date, optional): Data da reserva.
            start_time (datetime.time, optional): Horário de início.
            end_time (datetime.time, optional): Horário de término.
            purpose (str, optional): Objetivo da reserva.
            category_name (str, optional): Nome da categoria associada.
            observations (str, optional): Texto contido nas observações.
            active (bool, optional): Se a reserva está ativa ou cancelada.
        Returns:
            list[ReservationTable]: Lista de reservas encontradas.
    """
    with Session(engine) as session:
        query = select(ReservationTable).options(selectinload(ReservationTable.observers))
        
        if user:
            user_obj = session.execute(select(UserTable).where(UserTable.name == user)).scalar_one_or_none()
            if not user_obj:
                return []
            query = query.where(ReservationTable.user == user_obj.id)
            
        if artifact:
            artifact_obj = session.execute(select(ArtifactTable).where(ArtifactTable.name == artifact)).scalar_one_or_none()
            if not artifact_obj:
                return []
            query = query.where(ReservationTable.artifact == artifact_obj.id)
            
        if date:
            query = query.where(ReservationTable.date == date)
        if start_time:
            query = query.where(ReservationTable.start_time == start_time)
        if end_time:
            query = query.where(ReservationTable.end_time == end_time)
        if purpose:
            query = query.where(ReservationTable.purpose == purpose)
            
        if category_name:
            query = query.join(ArtifactTable).join(CategoryTable).where(CategoryTable.name == category_name)
            
        if observations:
            query = query.where(ReservationTable.observations.contains(observations))
        if active is not None:
            query = query.where(ReservationTable.active == active)
        
        return session.execute(query).scalars().all()

def batch_add_reservation(
        user: str, 
        artifact: str, 
        date_list: list[datetime.date], 
        start_time: datetime.time, 
        end_time: datetime.time, 
        purpose: str, 
        observations: str = None,
        observers: list[str] = None
    ):
    """ Cadastra reservas em lote para múltiplos dias em um único identificador (batch_id). 
    
        Args:
            user (str): Nome do usuário criador.
            artifact (str): Nome do artefato (sala/equipamento).
            date_list (list[datetime.date]): Lista de datas das reservas.
            start_time (datetime.time): Horário de início.
            end_time (datetime.time): Horário de término.
            purpose (str): Objetivo da reserva.
            observations (str, optional): Observações adicionais.
            observers (list[str], optional): Lista de nomes dos observadores.
        Returns:
            int: O identificador numérico gerado para o lote (batch_id).
    """
    with Session(engine) as session:
        user_obj = session.execute(select(UserTable).where(UserTable.name == user)).scalar_one()
        artifact_obj = session.execute(select(ArtifactTable).where(ArtifactTable.name == artifact)).scalar_one()
        
        batch_id = int(datetime.datetime.now().timestamp())
        
        for date in date_list:
            if get_reservation(user=user, artifact=artifact, date=date, start_time=start_time, end_time=end_time, active=True):
                print(f"Reservation already exists for the given parameters on date {date}.")
                continue

            reservation = ReservationTable(
                user=user_obj.id,
                artifact=artifact_obj.id,
                date=date,
                start_time=start_time,
                end_time=end_time,
                purpose=purpose,
                observations=observations,
                created_at=datetime.datetime.now(),
                batch_id=batch_id
            )
            
            if observers:
                for obs_name in observers:
                    obs_user = session.execute(select(UserTable).where(UserTable.name == obs_name)).scalar_one()
                    reservation.observers.append(obs_user)
                    
            session.add(reservation)
        session.commit()
        return batch_id

def cancel_reservation(reservation_id: int, canceler_user: str):
    """ Cancela uma reserva cadastrada e registra o usuário autor da ação. 
    
        Args:
            reservation_id (int): ID da reserva a ser cancelada.
            canceler_user (str): Nome do usuário que cancela a reserva.
        Returns:
            bool: True se a reserva foi encontrada e cancelada, False caso contrário.
    """
    with Session(engine) as session:
        reservation = session.get(ReservationTable, reservation_id)
        if reservation:
            user_obj = session.execute(select(UserTable).where(UserTable.name == canceler_user)).scalar_one()
            reservation.active = False
            reservation.canceler_user = user_obj.id
            session.commit()
            return True
        return False