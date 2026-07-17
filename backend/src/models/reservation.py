import datetime

from typing import Optional, List
from colour import Color
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import ColorType
from sqlalchemy import Date, Time, DateTime, ForeignKey, JSON

from models.database import Base

class UserTable(Base):
    """ Tabela de usuários. 
    
        Args:
            name (str): Nome do usuário.
            email (str): Email do usuário.
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)

class CategoryTable(Base):
    """ Tabela de categorias. 
    
        Args:
            name (str): Nome da categoria.
            color (Color): Cor associada à categoria.
    """
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    color: Mapped[Color] = mapped_column(ColorType)

class ArtifactTable(Base):
    """ Tabela de artefatos. 
    
        Args:
            name (str): Nome do artefato.
            description (Optional[str]): Descrição do artefato.
            category (int): ID da categoria do artefato.
    """
    __tablename__ = "artifacts"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[Optional[str]] = mapped_column()
    category: Mapped[int] = mapped_column(ForeignKey("categories.id"))

class ObserverTable(Base):
    """ Tabela de observadores. 
    
        Args:
            reservation_id (int): ID da reserva.
            user_id (int): ID do usuário observador.
    """
    __tablename__ = "observers"

    reservation_id: Mapped[int] = mapped_column(ForeignKey("reservations.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)

class ReservationTable(Base):
    """ Tabela de reservas. 
    
        Args:
            user (int): ID do usuário que fez a reserva.
            artifact (int): ID do artefato reservado.
            date (datetime.date): Data da reserva.
            start_time (datetime.time): Hora de início da reserva.
            end_time (datetime.time): Hora de término da reserva.
            purpose (str): Propósito da reserva.
            active (bool): Indica se a reserva está ativa ou cancelada.
            batch_id (Optional[int]): ID do lote, caso a reserva faça parte de um lote.
            observations (Optional[str]): Observações adicionais sobre a reserva.
            created_at (datetime.datetime): Data e hora de criação da reserva.
            canceler_user (Optional[int]): ID do usuário que cancelou a reserva, se aplicável.
    """

    __tablename__ = 'reservations'

    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[int] = mapped_column(ForeignKey("users.id"))
    artifact: Mapped[int] = mapped_column(ForeignKey("artifacts.id"))
    date: Mapped[datetime.date] = mapped_column(Date)
    start_time: Mapped[datetime.time] = mapped_column(Time)
    end_time: Mapped[datetime.time] = mapped_column(Time)
    purpose: Mapped[str] = mapped_column()
    active: Mapped[bool] = mapped_column(default=True)
    batch_id: Mapped[Optional[int]] = mapped_column(nullable=True)
    observations: Mapped[Optional[str]] = mapped_column(nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime)
    canceler_user: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    
    observers: Mapped[List["UserTable"]] = relationship(secondary="observers")