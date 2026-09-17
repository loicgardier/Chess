from .base import Base
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import Integer,ForeignKey

from enum import StrEnum,auto
from sqlalchemy.types import Enum

class Rencontres(Base):
    __tablename__="rencontres"

    class Resulats(StrEnum):
        Blanc=auto()
        Noir=auto()
        Equalite=auto()
        PasJoue=auto()

    id:Mapped[int] = mapped_column(Integer,primary_key=True)
    id_tournament:Mapped[int] = mapped_column(Integer,ForeignKey('tournaments.id'),nullable=False)
    id_user_blanc:Mapped[int] = mapped_column(Integer,ForeignKey('users.id'),nullable=False)
    id_user_noir:Mapped[int] = mapped_column(Integer,ForeignKey('users.id'),nullable=False)
    ronde:Mapped[int] = mapped_column(Integer,nullable=False)
    resultat:Mapped[Resulats] =mapped_column(Enum(Resulats),nullable=False)

    tournament: Mapped["Tournaments"] = relationship("Tournaments",back_populates="rencontres",uselist=False)  # pyright: ignore[reportUndefinedVariable]
    blanc: Mapped["Users"] = relationship("Users",back_populates="rencontres_blanc",uselist=False)  # pyright: ignore[reportUndefinedVariable]
    noir: Mapped["Users"] = relationship("Users",back_populates="rencontres_noir",uselist=False)  # pyright: ignore[reportUndefinedVariable]
