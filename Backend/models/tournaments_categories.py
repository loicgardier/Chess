from .base import Base
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import Integer,ForeignKey

class TournamentsCategories(Base):
    __tablename__="tournaments_categories"

    id_categorie:Mapped[int] = mapped_column(Integer,ForeignKey('categories.id'),primary_key=True)
    id_tournament:Mapped[int] = mapped_column(Integer,ForeignKey('tournaments.id'),primary_key=True)

    categorie : Mapped["Categories"] = relationship("Categories",back_populates="tournaments_categories",uselist=False)  # pyright: ignore[reportUndefinedVariable]
    tournament : Mapped["Tournaments"] = relationship("Tournaments",back_populates="tournaments_categories",uselist=False)  # pyright: ignore[reportUndefinedVariable]

    def __repr__(self):
        return f'<TournamentsCategories {self.id_tournament} - {self.id_categorie}>'