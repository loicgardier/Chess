from .base import Base
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import Integer,ForeignKey

class Inscriptions(Base):
    __tablename__="inscriptions"

    id_user:Mapped[int] = mapped_column(Integer,ForeignKey('users.id'),primary_key=True)
    id_tournament:Mapped[int] = mapped_column(Integer,ForeignKey('tournaments.id'),primary_key=True)

    user : Mapped["Users"] = relationship("Users",back_populates="inscriptions",uselist=False)  # pyright: ignore[reportUndefinedVariable]
    tournament : Mapped["Tournaments"] = relationship("Tournaments",back_populates="inscriptions",uselist=False)  # pyright: ignore[reportUndefinedVariable]

    def __repr__(self):
        return f'<Inscriptions {self.id_tournament} - {self.id_user}>'