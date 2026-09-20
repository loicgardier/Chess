import jwt
from dotenv import load_dotenv
import os
from secrets import token_urlsafe
from datetime import datetime,timezone,timedelta
from fastapi import Response
from repositories.refresh_token_repository import RefreshTokenRepository
from models.refresh_token import RefreshToken
from utils import hash_utils 

load_dotenv()
key=os.environ["KEY"]

def encode(user)->str:
    return jwt.encode(user,key,algorithm="HS256")

def decode(token:str)->dict:
    return jwt.decode(token,key,algorithms="HS256")

def create_and_store_refresh_token(username: str,refresh_token_repository:RefreshTokenRepository) -> str:
    """Génère un Refresh Token Opaque et le stocke en Base de Données."""
    token_string = token_urlsafe(64)
    expires_at = datetime.now(timezone.utc) + timedelta(days=int(os.environ['REFRESH_TOKEN_EXPIRE_DAYS']))
    refresh_token= RefreshToken()
    refresh_token.id=token_string
    refresh_token.expires_at=expires_at
    refresh_token.username=username
    refresh_token_repository.add(refresh_token)
    return token_string

def set_refresh_cookie(response: Response, refresh_token: str):
    """Configure le cookie HTTP-Only pour le cross-domain."""
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True, 
        samesite="none",
        max_age=int(os.environ['REFRESH_TOKEN_EXPIRE_DAYS']) * 24 * 3600,
        path="/users"
    )