from fastapi import FastAPI,APIRouter,Body,Depends,HTTPException
from dtos.user_inscription_request import UserInscriptionRequest
from dtos.user_inscription_response import UserInscriptionReponse
from repositories.users_repository import UsersRepository
from utils import jwt_utils  
from exceptions.users_exceptions import ExistingPseudo,ExistingMail,ExistingMailPseudo

user_router = APIRouter(prefix="/users",tags=["users"])


@user_router.post('/inscription')
async def inscription(
    user:UserInscriptionRequest = Body(),
    user_repository:UsersRepository=Depends(UsersRepository)
    )->UserInscriptionReponse:
    try:
        user_repository.add(user.to_user_model())
        response =UserInscriptionReponse
        response.token = jwt_utils.encode(user)
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
#    except:
#        raise HTTPException(status_code=500)

@user_router.post('/conection')
async def conection():
    pass

#def update_profile