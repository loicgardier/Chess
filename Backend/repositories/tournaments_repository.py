from datetime import datetime
from exceptions.tournaments_exceptions import IsAlreadyRegisterException,IsNotRegisteredException
from sqlalchemy.orm import Session
from models.tournaments_categories import TournamentsCategories
from models.inscriptions import Inscriptions
from models.users import Users
from models.tournaments import Tournaments
from models.categories import Categories
from utils.session_utils import get_session
from fastapi import Depends

class TournamentsRepository:

    def __init__(self,session:Session=Depends(get_session)):
        self.__session=session

    def get_one(self,id:int)->Tournaments|None:
        return self.__session.get(Tournaments,id)

    def get_ten(self)->list[Tournaments]:
        return self.__session.query(Tournaments)\
            .where(Tournaments.status!=Tournaments.Status.Termine)\
            .order_by(Tournaments.date_de_derniere_mise_a_jour.desc())\
            .limit(10).all()

    def get_all(self)->list[Tournaments]:
        return self.__session.query(Tournaments).all()

    def get_categories(self)->list[TournamentsCategories]:
        return self.__session.query(TournamentsCategories).all()

    def get_nb_inscript(self,id:int)->int:
        return self.__session.query(Inscriptions).where(Inscriptions.id_tournament==id).count()

    def add(self,tournament:Tournaments,categories:list[int])->Tournaments:
        self.__session.add(tournament)
        self.__session.flush()
        for id in categories:
            tournament_categorie=TournamentsCategories()
            tournament_categorie.id_tournament=tournament.id
            tournament_categorie.id_categorie=id
            self.__session.add(tournament_categorie)
        self.__session.commit()
        self.__session.refresh(tournament)
        return Tournaments
        
    def update(self,tournament:Tournaments,categories:list[int])->Tournaments|None:
        tournament_to_modify= self.get_one(tournament.id)
        if tournament_to_modify:
            #update categorie
            self.__session.query(TournamentsCategories).where(TournamentsCategories.id_tournament==tournament_to_modify.id).delete()
            self.__session.flush()
            for id in categories:
                tournament_categorie=TournamentsCategories()
                tournament_categorie.id_tournament=tournament_to_modify.id
                tournament_categorie.id_categorie=id
                self.__session.add(tournament_categorie)

            

            tournament_to_modify.nom=tournament.nom
            tournament_to_modify.lieu=tournament.lieu
            #check no conflict with existing player in tournament
            tournament_to_modify.elo_min=tournament.elo_min
            tournament_to_modify.elo_max=tournament.elo_max
            tournament_to_modify.inscript_min=tournament.inscript_min
            tournament_to_modify.inscript_max=tournament.inscript_max
            tournament_to_modify.women_only=tournament.women_only

            tournament_to_modify.date_de_fin_inscription=tournament.date_de_fin_inscription
            tournament_to_modify.date_de_derniere_mise_a_jour=datetime.now()

            self.__session.commit()
            self.__session.refresh(tournament_to_modify)
            return tournament_to_modify
        return None

    def change_status(self,id:int,status:Tournaments.Status)->Tournaments|None:
        tournament_to_modify= self.get_one(id)
        if tournament_to_modify:
            tournament_to_modify.status=status
            tournament_to_modify.date_de_derniere_mise_a_jour=datetime.now()
            self.__session.commit()
            self.__session.refresh(tournament_to_modify)


    def delete(self,id:int)->bool:
        tournament_to_delete=self.get_one(id)
        if tournament_to_delete and tournament_to_delete.status==Tournaments.Status.EnAttente:
            self.__session.query(Inscriptions).where(Inscriptions.id_tournament==id).delete()
            self.__session.query(TournamentsCategories).where(TournamentsCategories.id_tournament==tournament_to_delete.id).delete()
            self.__session.flush()
            self.__session.delete(tournament_to_delete)
            self.__session.commit()
            return True
        return False

    def can_register(self,id_user:int,id_tournament:int)->bool:
        tournament = self.__session.get_one(Tournaments,id_tournament)
        user = self.__session.get_one(Users,id_user)
        nb_inscript =  self.get_nb_inscript(id_tournament)
        now =datetime.now()

        age = now.year - user.date_de_naissance.year
        age_condition=False
        if(user.date_de_naissance.month<now.month or (user.date_de_naissance.month== now.month and user.date_de_naissance.day<now.day)):
            age =age -1

        categories = self.__session.query(Categories)\
                                .join(TournamentsCategories,TournamentsCategories.id_categorie==Categories.id)\
                                .where(TournamentsCategories.id_tournament==id_tournament).all()
        if len(categories)==0:
            age_condition=True
        else:
            for category in categories:
                if age>=category.age_min and age<=category.age_max:
                    age_condition=True

        return tournament and user and\
            user.elo<=tournament.elo_max and user.elo>=tournament.elo_min and\
            ((tournament.women_only and user.genre==Users.Genders.Femme)or not tournament.women_only ) and\
            tournament.date_de_fin_inscription>datetime.now() and tournament.status==Tournaments.Status.EnAttente and\
            nb_inscript<tournament.inscript_max and age_condition


    def register_user(self,id_user:int,id_tournament:int)->bool:
        if self.is_registered(id_user,id_tournament):
            raise IsAlreadyRegisterException()
        if self.can_register(id_user,id_tournament):
            inscription=Inscriptions()
            inscription.id_user=id_user
            inscription.id_tournament=id_tournament
            self.__session.add(inscription)
            self.__session.commit()
            return True
        return False

    def is_registered(self,id_user:int,id_tournament:int)->bool:
        try:
            self.__session.get_one(Inscriptions,{'id_user':id_user,'id_tournament':id_tournament})
            return True
        except:
            return False


    def unregister_user(self,id_user:int,id_tournament:int)->bool:
        tournament = self.__session.get_one(Tournaments,id_tournament)
        if tournament and tournament.status==Tournaments.Status.EnAttente:

            if self.is_registered(id_user,id_tournament):
                inscription=Inscriptions()
                inscription.id_tournament=id_tournament
                inscription.id_user=id_user
                self.__session.delete(inscription)
                self.__session.commit()
                return True
            else:
                raise IsNotRegisteredException()
        return False