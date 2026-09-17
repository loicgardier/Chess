from .base import Base
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import String,Integer,CheckConstraint,DateTime,Boolean
from datetime import datetime

from enum import StrEnum,auto
from sqlalchemy.types import Enum

class Users(Base):
    __tablename__='users'

    class Genders(StrEnum):
        Homme=auto()
        Femme=auto()
        Autre=auto()

    class Roles(StrEnum):
        Admin=auto()
        User=auto()

    id:Mapped[int] = mapped_column(Integer,primary_key=True)
    pseudo:Mapped[str] = mapped_column(String,unique=True,nullable=False)
    email:Mapped[str] = mapped_column(String,unique=True,nullable=False)
    password:Mapped[str] = mapped_column(String,nullable=False)
    genre:Mapped[Genders] = mapped_column(Enum(Genders),nullable=False)
    elo:Mapped[int] = mapped_column(Integer,CheckConstraint(sqltext='elo BETWEEN 0 AND 3000',name='ELO_CK'),nullable=False,default=1200)
    role:Mapped[Roles] = mapped_column(Enum(Roles),nullable=False,default=Roles.User)
    date_de_naissance: Mapped[datetime] = mapped_column(DateTime,nullable=False)
    allow_mail:Mapped[bool] =mapped_column(Boolean,nullable=False,default=False)

    inscriptions : Mapped[list["Inscription"]] = relationship("Inscription",back_populates="user") # pyright: ignore[reportUndefinedVariable]
    rencontres_blanc: Mapped[list["Rencontres"]] = relationship("Rencontres",back_populates="blanc") # pyright: ignore[reportUndefinedVariable]
    rencontres_noir: Mapped[list["Rencontres"]] = relationship("Rencontres",back_populates="noir") # pyright: ignore[reportUndefinedVariable]
