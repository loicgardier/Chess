from .base import Base
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import String,Integer,CheckConstraint,DateTime,Boolean
from datetime import datetime


class Categories(Base):
    __tablename__='categories'

    id:Mapped[int] = mapped_column(Integer,primary_key=True)
    name:Mapped[str] = mapped_column(String,unique=True,nullable=False)

    tournaments_categories : Mapped[list["TournamentsCategories"]] = relationship("TournamentsCategories",back_populates="categorie") # pyright: ignore[reportUndefinedVariable]

    def __repr__(self):
        return f'<Categories {self.id}>'