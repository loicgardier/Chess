from fastapi import APIRouter,Body,Depends,HTTPException,Response,Request
from dtos.user_inscription_request import UserInscriptionRequest
from dtos.user_inscription_response import UserInscriptionReponse
from dtos.user_connection_request import UserConnectionRequest
from dtos.user_connection_response import UserConnectionReponse
from repositories.users_repository import UsersRepository
from repositories.refresh_token_repository import RefreshTokenRepository
from utils import jwt_utils  
from exceptions.users_exceptions import ExistingPseudo,ExistingMail,ExistingMailPseudo,UnknowMailPseudo
from argon2.exceptions import VerifyMismatchError
from services.mailer import Mailer
from pathlib import Path
from datetime import datetime,timezone

user_router = APIRouter(prefix="/users",tags=["users"])


@user_router.post('/inscription')
async def inscription(
    response:Response,
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
        refresh_token = jwt_utils.create_and_store_refresh_token(user_added.pseudo)
        jwt_utils.set_refresh_cookie(response,refresh_token)
        access_token =UserInscriptionReponse()
        access_token.token = jwt_utils.encode(user_added.to_jwt())

        return access_token
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
        response:Response,
        user:UserConnectionRequest = Body(),
        user_repository:UsersRepository=Depends(UsersRepository)
    ):
    try:
        if user_repository.verify(user.pseudo_or_mail,user.password):
            user_db=user_repository.get_by_mail_or_pseudo(user.pseudo_or_mail)
            refresh_token = jwt_utils.create_and_store_refresh_token(user_db.pseudo)
            jwt_utils.set_refresh_cookie(response,refresh_token)
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
    except:
        raise HTTPException(status_code=500)

@user_router.post("/refresh")
async def refresh_access_token(
    request: Request,
    response: Response,
    refresh_token_repository:RefreshTokenRepository=Depends(RefreshTokenRepository),
     user_repository:UsersRepository=Depends(UsersRepository)
    )->UserConnectionReponse:
    refresh_token = request.cookies.get("refresh_token")
    token_data=refresh_token_repository.get_by_username(refresh_token)
    if not token_data:
        raise HTTPException(
            status_code=401,
            detail="Refresh token manquant ou inconnu."
        )
    if token_data.is_revoked:
        response.delete_cookie(key="refresh_token", path="/users", samesite="none",secure=True)
        raise HTTPException(
            status_code=401,
            detail="Alerte sécurité : Tentative de réutilisation d'un jeton. Session bloquée."
        )
    if datetime.now(timezone.utc) > token_data["expires_at"]:
        refresh_token_repository.revoke(token_data.id)
        response.delete_cookie(key="refresh_token", path="/users", samesite="none",secure=True)
        raise HTTPException(
            status_code=401,
            detail="Session expirée. Veuillez vous reconnecter."
        )
    refresh_token_repository.revoke(token_data.id)

    user=user_repository.get_by_mail_or_pseudo(token_data.username)
    new_access_token = jwt_utils.encode(user=user.to_jwt())
    new_refresh_token = jwt_utils.create_and_store_refresh_token(token_data.username)
    # Inserer le nouveau cookie de rotation
    jwt_utils.set_refresh_cookie(response, new_refresh_token)
    return UserConnectionReponse(token=new_access_token)

    #def update_profile