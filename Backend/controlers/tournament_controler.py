from fastapi import APIRouter,Body,Depends,HTTPException
from repositories.tournaments_repository import TournamentsRepository
from utils import jwt_utils  
from exceptions.users_exceptions import ExistingPseudo
from services.mailer import Mailer
from pathlib import Path
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials 
import jwt

tournament_router = APIRouter(prefix="/tournaments",tags=["tournaments"])

security = HTTPBearer()

@tournament_router.get('/')
async def get_tournaments(
    tournament_repository:TournamentsRepository=Depends(TournamentsRepository),
    token:HTTPAuthorizationCredentials =Depends(security)):
    try:
        payload = jwt_utils.decode(token.credentials)
        print(payload)

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401,detail="Jeton d'accès expiré.",headers={"WWW-Authenticate": "Bearer"})
    except jwt.InvalidSignatureError:
        raise HTTPException(status_code=401,detail="Signature du jeton d'accès invalide.",headers={"WWW-Authenticate": "Bearer"})
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=401,detail=f"Jeton d'accès invalide:{e}",headers={"WWW-Authenticate": "Bearer"})
