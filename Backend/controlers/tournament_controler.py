from fastapi import APIRouter,Body,Depends,HTTPException
from repositories.tournaments_repository import TournamentsRepository
from repositories.categories_repository import CategoriesRepository
from repositories.users_repository import UsersRepository
from utils import jwt_utils  
from exceptions.jwt_exceptions import NotAdminException
from exceptions.tournaments_exceptions import IsAlreadyRegisterException,IsNotRegisteredException
from services.mailer import Mailer
from pathlib import Path
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials 
from dtos.tournament_get_tournaments_reponse import TournamentGetTournamentResponse
from models.users import Users
from dtos.tournament_create_tournament_request import TournamentCreateTournamentRequest
import jwt

tournament_router = APIRouter(prefix="/tournaments",tags=["tournaments"])

security_lax = HTTPBearer(auto_error=False)
security = HTTPBearer()

@tournament_router.get('/')
async def get_tournaments(
    tournament_repository:TournamentsRepository=Depends(TournamentsRepository),
    user_repository:UsersRepository=Depends(UsersRepository),
    category_repository:CategoriesRepository=Depends(CategoriesRepository),
    token:HTTPAuthorizationCredentials =Depends(security_lax))->list[TournamentGetTournamentResponse]:
    username=None
    if token:
        try:
            payload = jwt_utils.decode(token.credentials)
            username=payload.get('pseudo')

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401,detail="Jeton d'accès expiré.",headers={"WWW-Authenticate": "Bearer"})
        except jwt.InvalidSignatureError:
            raise HTTPException(status_code=401,detail="Signature du jeton d'accès invalide.",headers={"WWW-Authenticate": "Bearer"})
        except jwt.PyJWTError as e:
            raise HTTPException(status_code=401,detail=f"Jeton d'accès invalide:{e}",headers={"WWW-Authenticate": "Bearer"})
    data_response =[]

    tournaments=tournament_repository.get_ten()
    for tournament in tournaments:
        tournament_data =TournamentGetTournamentResponse.from_model(tournament_repository,user_repository,category_repository,tournament.id,username)
        data_response.append(tournament_data)
    return data_response

@tournament_router.post('/')
async def create_tournament(
    tournament:TournamentCreateTournamentRequest=Body(),
    tournament_repository:TournamentsRepository=Depends(TournamentsRepository),
    categories_repository:CategoriesRepository=Depends(CategoriesRepository),
    token:HTTPAuthorizationCredentials=Depends(security)
    ):
    try:
        payload = jwt_utils.decode(token.credentials)
        role=payload.get('role')
        if role!=Users.Roles.Admin:
                raise NotAdminException()
        categories=[]
        categories_name=tournament.get_categories()
        for category_name in categories_name:
            categories.append(categories_repository.get_one_by_name(category_name.name).id)
        tournament_repository.add(tournament.to_tournament_model(),categories)
    except NotAdminException:
        raise HTTPException(status_code=403,detail=f"Role requis:{Users.Roles.Admin}")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401,detail="Jeton d'accès expiré.",headers={"WWW-Authenticate": "Bearer"})
    except jwt.InvalidSignatureError:
        raise HTTPException(status_code=401,detail="Signature du jeton d'accès invalide.",headers={"WWW-Authenticate": "Bearer"})
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=401,detail=f"Jeton d'accès invalide:{e}",headers={"WWW-Authenticate": "Bearer"})

@tournament_router.post('/{id}/register')
async def register(
    id:int=Path(),
    tournament_repository:TournamentsRepository=Depends(TournamentsRepository),
    user_repository:UsersRepository=Depends(UsersRepository),
    token:HTTPAuthorizationCredentials =Depends(security)
    ):
    try:
        payload = jwt_utils.decode(token.credentials)
        username=payload.get('pseudo')
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401,detail="Jeton d'accès expiré.",headers={"WWW-Authenticate": "Bearer"})
    except jwt.InvalidSignatureError:
        raise HTTPException(status_code=401,detail="Signature du jeton d'accès invalide.",headers={"WWW-Authenticate": "Bearer"})
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=401,detail=f"Jeton d'accès invalide:{e}",headers={"WWW-Authenticate": "Bearer"})
    try:
        user= user_repository.get_by_mail_or_pseudo(username)
        if tournament_repository.register_user(user.id,id):
            return
        else:
            raise HTTPException(status_code=400,detail=f"Impossible d'enregistrer {username} au tournoi")
    except IsAlreadyRegisterException:
        raise HTTPException(status_code=400,detail=f"{username} est déjà inscript au tournoi")


@tournament_router.post('/{id}/unregister')
async def unregister(
    id:int=Path(),
    tournament_repository:TournamentsRepository=Depends(TournamentsRepository),
    user_repository:UsersRepository=Depends(UsersRepository),
    token:HTTPAuthorizationCredentials =Depends(security)
    ):
    try:
        payload = jwt_utils.decode(token.credentials)
        username=payload.get('pseudo')
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401,detail="Jeton d'accès expiré.",headers={"WWW-Authenticate": "Bearer"})
    except jwt.InvalidSignatureError:
        raise HTTPException(status_code=401,detail="Signature du jeton d'accès invalide.",headers={"WWW-Authenticate": "Bearer"})
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=401,detail=f"Jeton d'accès invalide:{e}",headers={"WWW-Authenticate": "Bearer"})
    try:
        user= user_repository.get_by_mail_or_pseudo(username)
        if tournament_repository.unregister_user(user.id,id):
            return
        else:
            raise HTTPException(status_code=400,detail=f"Impossible de supprimer l'inscription de {username} au tournoi")
    except IsNotRegisteredException:
        raise HTTPException(status_code=400,detail=f"{username} n'est pas inscript au tournoi")