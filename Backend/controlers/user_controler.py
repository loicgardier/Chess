from fastapi import APIRouter,Body,Depends,HTTPException
from dtos.user_inscription_request import UserInscriptionRequest
from dtos.user_inscription_response import UserInscriptionReponse
from dtos.user_connection_request import UserConnectionRequest
from dtos.user_connection_response import UserConnectionReponse
from repositories.users_repository import UsersRepository
from utils import jwt_utils  
from exceptions.users_exceptions import ExistingPseudo,ExistingMail,ExistingMailPseudo,UnknowMailPseudo
from argon2.exceptions import VerifyMismatchError
from services.mailer import Mailer
from pathlib import Path

user_router = APIRouter(prefix="/users",tags=["users"])


@user_router.post('/inscription')
async def inscription(
    user:UserInscriptionRequest = Body(),
    user_repository:UsersRepository=Depends(UsersRepository),
    mailer:Mailer=Depends(Mailer)
    )->UserInscriptionReponse:
    try:
        user_added=user_repository.add(user.to_user_model())
        template_path = Path("Backend/templates/inscription.html")
        body=template_path.read_text("utf-8")
        body =body.format(name=user.pseudo)
        mailer.send_mail('Crétion du compte',user.email,body)
        response =UserInscriptionReponse()
        response.token = jwt_utils.encode(user_added.to_jwt())

        return response
    except ExistingMail:
        raise HTTPException(status_code=422,detail=[
            {
            "loc": ["body","email"],
            "msg": "Email is already existing",
            "type": "value_error",
            "input": user.email,
            }
        ])
    except ExistingPseudo:
        raise HTTPException(status_code=422,detail=[
            {
            "loc": ["body","pseudo"],
            "msg": "Pseudo is already existing",
            "type": "value_error",
            "input": user.pseudo,
            }
        ])
    except ExistingMailPseudo:
        raise HTTPException(status_code=422,detail=[
            {
            "loc": ["body","pseudo"],
            "msg": "Pseudo is already existing",
            "type": "value_error",
            "input": user.pseudo,
            },
            {
            "loc": ["body","email"],
            "msg": "Email is already existing",
            "type": "value_error",
            "input": user.email,
            }
        ])
    #except:
    #    raise HTTPException(status_code=500)

@user_router.post('/conection')
async def conection(
        user:UserConnectionRequest = Body(),
        user_repository:UsersRepository=Depends(UsersRepository)
    ):
    try:
        if user_repository.verify(user.pseudo_or_mail,user.password):
            user_db=user_repository.get_by_mail_or_pseudo(user.pseudo_or_mail)
            response =UserConnectionReponse()
            response.token = jwt_utils.encode(user_db.to_jwt())
            return response
    except VerifyMismatchError:
            raise HTTPException(status_code=422,detail=[
                {
                "loc": ["body","password"],
                "msg": "password is not valid",
                "type": "value_error",
                "input": '',
                }
            ])
    except UnknowMailPseudo:
        raise HTTPException(status_code=422,detail=[
            {
            "loc": ["body","pseudo_or_mail"],
            "msg": "Email or pseudo is unknown",
            "type": "value_error",
            "input": user.pseudo_or_mail,
            }
        ])
    #except:
    #    raise HTTPException(status_code=500)
    

#def update_profile