from sqlalchemy.orm import Session
from models.users import Users
from utils import hash_utils
from sqlalchemy import or_
from fastapi import Depends
from utils.session_utils import get_session
from exceptions.users_exceptions import ExistingMail,ExistingMailPseudo,ExistingPseudo

class UsersRepository:

    def __init__(self,session:Session=Depends(get_session)):
        self.__session=session

    def get_one(self,id:int)->Users|None:
        self.__session.get(Users,id)

    def get_all(self)->list[Users]:
        return self.__session.query(Users).all()

    def verify(self,id:str,password:str)->bool:
        user = self.__session.query(Users).where(or_(Users.pseudo==id,Users.email==id)).first()
        if user:
            return hash_utils.verify(user.password,password)
        return False

    def add(self,user:Users)->Users:

        pseudo = self.__session.query(Users).where(Users.pseudo==user.pseudo).first()
        email = self.__session.query(Users).where(Users.email==user.email).first()
        if pseudo and email:
            raise ExistingMailPseudo()
        elif email:
            raise ExistingMail()
        elif pseudo:
            raise ExistingPseudo()

        user.password=hash_utils.hash(user.password)
        self.__session.add(user)
        self.__session.commit()
        self.__session.refresh(user)
        return user
        
    def update(self,user:Users)->Users|None:
        user_to_modify= self.get_one(user.id)
        if user_to_modify:
            user_to_modify.pseudo=user.pseudo
            user_to_modify.email=user.email
            user_to_modify.password=hash_utils.hash(user.password)
            user_to_modify.genre=user.genre
            user_to_modify.elo=user.elo
            user_to_modify.role=user.role
            user_to_modify.date_de_naissance=user.date_de_naissance
            user_to_modify.allow_mail=user.allow_mail
            self.__session.commit()
            self.__session.refresh(user_to_modify)
            return user_to_modify
        return None

    def update_elo(self,id:int,elo:int)->Users:
        user=self.get_one(id)
        user.elo=elo
        self.__session.commit()
        self.__session.refresh(user)
        return user

    def delete(self,id:int)->Users:
        pass