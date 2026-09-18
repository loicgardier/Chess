import jwt
from dotenv import load_dotenv,get_key

load_dotenv()
key=get_key('.env','KEY')

def encode(user):
    return jwt.encode(user,key,algorithm="HS256")

def decode(token:str):
    return jwt.decode(token,key,algorithms="HS256")