from fastapi import APIRouter,Body,Depends,HTTPException
from repositories.rencontres_repository import RencontresRepository
from utils import jwt_utils  
from exceptions.jwt_exceptions import NotAdminException
from pathlib import Path
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials 
from models.rencontres import Rencontres
from models.users import Users
from exceptions.rencontres_exceptions import RencontresNonExistant,RondeFinie

import jwt

match_router = APIRouter(prefix="/tournaments",tags=["match"])

security = HTTPBearer()

@match_router.post('/{id}')
async def set_match_result(
    id:int=Path(),
    result:Rencontres.Resulats=Body(),
    rencontre_repository:RencontresRepository=Depends(RencontresRepository),
    token:HTTPAuthorizationCredentials =Depends(security)
):
    try:
            payload = jwt_utils.decode(token.credentials)
            role=payload.get('role')
            if role!=Users.Roles.Admin:
                    raise NotAdminException()
            if rencontre_repository.change_result(id,result):
                 return
            else:
                 raise HTTPException(status_code=500,detail='Erreur lors du changement de resultat')
    except NotAdminException:
        raise HTTPException(status_code=403,detail=f"Role requis:{Users.Roles.Admin}")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401,detail="Jeton d'accès expiré.",headers={"WWW-Authenticate": "Bearer"})
    except jwt.InvalidSignatureError:
        raise HTTPException(status_code=401,detail="Signature du jeton d'accès invalide.",headers={"WWW-Authenticate": "Bearer"})
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=401,detail=f"Jeton d'accès invalide:{e}",headers={"WWW-Authenticate": "Bearer"})
    except RencontresNonExistant:
         raise HTTPException(status_code=400,detail="La rencontre choisie n'existe pas")
    except RondeFinie:
         raise HTTPException(status_code=400,detail="La rencontre choisie fait partie d'une ronde déjà jouée")