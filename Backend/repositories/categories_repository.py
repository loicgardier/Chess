from datetime import datetime

from sqlalchemy.orm import Session
from models.tournaments_categories import TournamentsCategories
from models.inscriptions import Inscriptions
from models.categories import Categories
from models.tournaments_categories import TournamentsCategories
from utils.session_utils import get_session
from fastapi import Depends

class CategoriesRepository:

    def __init__(self,session:Session=Depends(get_session)):
        self.__session=session

    def get_one(self,id:int)->Categories|None:
        return self.__session.get(Categories,id)
    def get_one_by_name(self,name:str)->Categories|None:
        return self.__session.query(Categories).where(Categories.name==name).first()
    def get_by_tournament(self,id:int)->list[TournamentsCategories]:
        return self.__session.query(TournamentsCategories).where(TournamentsCategories.id_tournament==id).all()
    def get_all(self)->list[Categories]:
        return self.__session.query(Categories).all()