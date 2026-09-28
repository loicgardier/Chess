from pydantic import BaseModel,EmailStr,SecretStr,Field
from models.users import Users
from datetime import datetime,date

class UserInscriptionRequest(BaseModel):

    pseudo:str =Field(description="User pseudo")
    email:EmailStr =Field(description="User email")
    password:SecretStr =Field(description="User password")
    genre:Users.Genders =Field(description="User gender")
    elo:int | None =Field(description="User pseudo",default=1200)
    date_de_naissance: date = Field(description="User birthdate")
    allow_mail:bool = Field(description='Allow to send mail to user')


    def to_user_model(self)->Users:
        user=Users()
        user.pseudo=self.pseudo
        user.email=self.email
        user.password=self.password
        user.genre=self.genre
        user.elo=self.elo
        user.role=Users.Roles.User
        user.date_de_naissance=datetime(self.date_de_naissance.year,self.date_de_naissance.month,self.date_de_naissance.day)
        user.allow_mail=self.allow_mail
        return user