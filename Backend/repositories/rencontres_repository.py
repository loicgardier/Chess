
from datetime import datetime

from sqlalchemy.orm import Session,aliased
from models.tournaments import Tournaments
from models.rencontres import Rencontres
from models.users import Users
from utils.session_utils import get_session
from fastapi import Depends
from exceptions.rencontres_exceptions import RencontresNonExistant,RondeFinie

class RencontresRepository:

    def __init__(self,session:Session=Depends(get_session)):
        self.__session=session

    def get_one(self,id:int)->Rencontres:
        return self.__session.get_one(Rencontres,id)

    def get_by_roud(self,id_tournament:int)->list[tuple[Rencontres, str, str]]:
        blanc = aliased(Users)
        noir = aliased(Users)
        return self.__session.query(Rencontres,blanc.pseudo,noir.pseudo)\
            .join(Tournaments,Rencontres.id_tournament==Tournaments.id)\
            .join(blanc,blanc.id==Rencontres.id_user_blanc)\
            .join(noir,noir.id==Rencontres.id_user_noir)\
            .where(Rencontres.id_tournament==id_tournament)\
            .where(Rencontres.ronde==Tournaments.ronde)\
            .all()

    def get_all(self)->list[Rencontres]:
        return self.__session.query(Rencontres).all()   

    def change_result(self,id:int,result:Rencontres.Resulats)->bool:
        try:
            rencontre = self.__session.get_one(Rencontres,id)
            tournament = self.__session.query(Tournaments).where(Tournaments.id==rencontre.id_tournament).where(Tournaments.ronde==rencontre.ronde).first()
            if tournament:
                rencontre.resultat=result
                self.__session.commit()
                return True
            else:
                raise RondeFinie()
        except:
            raise RencontresNonExistant()
