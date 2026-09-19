from .base import Base
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import String,Integer,DateTime,Boolean
from datetime import datetime

from enum import StrEnum,auto
from sqlalchemy.types import Enum

class Tournaments(Base):
    __tablename__="tournaments"

    class Categories(StrEnum):
        Junior=auto()
        Senior=auto()
        Veteran=auto()

    class Status(StrEnum):
        EnAttente=auto()
        EnCours=auto()
        Termine=auto()

    id:Mapped[int] = mapped_column(Integer,primary_key=True)
    nom:Mapped[str] = mapped_column(String,nullable=False)
    lieu:Mapped[str] = mapped_column(String)
    inscript_min:Mapped[int] = mapped_column(Integer,nullable=False,default=2)
    inscript_max:Mapped[int] = mapped_column(Integer,nullable=False,default=32)
    elo_min:Mapped[int] = mapped_column(Integer,nullable=True)
    elo_max:Mapped[int] = mapped_column(Integer,nullable=True)
    status:Mapped[Status] = mapped_column(Enum(Status),nullable=False,default=Status.EnAttente)
    ronde:Mapped[int] = mapped_column(Integer,nullable=False,default=0)
    women_only:Mapped[bool] =mapped_column(Boolean,nullable=False,default=False)
    date_de_creation: Mapped[datetime] = mapped_column(DateTime,nullable=False,default=datetime.now())
    date_de_fin_inscription: Mapped[datetime] = mapped_column(DateTime,nullable=False)
    date_de_derniere_mise_a_jour: Mapped[datetime] = mapped_column(DateTime,nullable=False)

    inscriptions : Mapped[list["Inscriptions"]] = relationship("Inscription",back_populates="tournament") # pyright: ignore[reportUndefinedVariable]
    rencontres : Mapped[list["Rencontres"]] = relationship("Rencontres",back_populates="tournament") # pyright: ignore[reportUndefinedVariable]
    tournaments_categories : Mapped[list["TournamentsCategories"]] = relationship("TournamentsCategories",back_populates="tournament") # pyright: ignore[reportUndefinedVariable]

    def __repr__(self):
        return f'<Tournaments {self.id}>'