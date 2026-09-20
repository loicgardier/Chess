import jwt
from dotenv import load_dotenv
import os

load_dotenv()
key=os.environ["KEY"]

def encode(user)->str:
    return jwt.encode(user,key,algorithm="HS256")

def decode(token:str)->dict:
    return jwt.decode(token,key,algorithms="HS256")