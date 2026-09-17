from .base import Base
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import Integer,ForeignKey

class Inscription(Base):
    __tablename__="inscription"

    id_user:Mapped[int] = mapped_column(Integer,ForeignKey('users.id'),primary_key=True)
    id_tournament:Mapped[int] = mapped_column(Integer,ForeignKey('tournaments.id'),primary_key=True)

    users : Mapped["Users"] = relationship("users",back_populates="inscriptions",uselist=False)  # pyright: ignore[reportUndefinedVariable]
    tournaments : Mapped["Tournaments"] = relationship("tournaments",back_populates="inscriptions",uselist=False)  # pyright: ignore[reportUndefinedVariable]
