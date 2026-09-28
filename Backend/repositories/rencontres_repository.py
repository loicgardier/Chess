
from datetime import datetime

from sqlalchemy.orm import Session
from models.tournaments import Tournaments
from models.rencontres import Rencontres


class RencontresRepository:

    def __init__(self,session:Session):
        self.__session=session

    def get_one(self,id:int)->Rencontres:
        return self.__session.get_one(Rencontres,id)

    def get_by_roud(self,id_tournament:int,ronde:int)->list[Rencontres]:
        return self.__session.query(Rencontres).where(Rencontres.id_tournament==id_tournament).where(Rencontres.ronde==ronde).all()

    def get_all(self)->list[Rencontres]:
        return self.__session.query(Rencontres).all()

    def get_score(self):
        pass
    
    def change_round(self,id:int)->Tournaments|None:
        tournament_to_modify= self.__session.get_one(Tournaments,id)
        if tournament_to_modify:
            #check rencontre
            round_unfinished = self.__session.query(Rencontres).where(Rencontres.id_tournament==id)\
                .where(Rencontres.ronde==tournament_to_modify.ronde)\
                .where(Rencontres.resultat==Rencontres.Resulats.PasJoue).count()
            if round_unfinished==0:
                tournament_to_modify.ronde=tournament_to_modify.ronde+1
                tournament_to_modify.date_de_derniere_mise_a_jour=datetime.now()
                self.__session.commit()
                self.__session.refresh(tournament_to_modify)

    def change_result(self,id:int,result:Rencontres.Resulats)->bool:
        rencontre = self.__session.get_one(Rencontres,id)
        if rencontre:
            rencontre.resultat=result
            self.__session.commit()
            return True
        return False

    def generate_round(self):
        pass
