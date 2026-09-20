from .base import Base
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import String,Integer,DateTime,Boolean
from datetime import datetime



class RefreshToken(Base):
    __tablename__='refresh_token'


    id:Mapped[str] = mapped_column(String,primary_key=True,autoincrement=False)
    username:Mapped[str] = mapped_column(String,unique=True,nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime,nullable=False)
    is_revoked:Mapped[bool] =mapped_column(Boolean,nullable=False,default=False)

    def __repr__(self):
        return f'<RefreshToken {self.id}>'

