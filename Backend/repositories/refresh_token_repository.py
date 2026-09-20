from sqlalchemy.orm import Session
from models.refresh_token import RefreshToken
from fastapi import Depends
from utils.session_utils import get_session
from datetime import datetime

class RefreshTokenRepository:

    def __init__(self,session:Session=Depends(get_session)):
        self.__session=session

    def get_one(self,id:int)->RefreshToken|None:
        self.__session.get(RefreshToken,id)

    def get_by_username(self,username:str)->RefreshToken|None:
        return self.__session.query(RefreshToken).where(RefreshToken.username==str).where(RefreshToken.expires_at>datetime.now()).first()

    def add(self,refresh:RefreshToken)->RefreshToken:
        self.__session.add(refresh)
        self.__session.commit()
        self.__session.refresh(refresh)
        return refresh
        
    def revoke(self,id:int)->RefreshToken|None:
        refresh_to_modify= self.get_one(id)
        if refresh_to_modify:
            refresh_to_modify.is_revoked=True
            self.__session.commit()
            self.__session.refresh(refresh_to_modify)
            return refresh_to_modify
        return None
