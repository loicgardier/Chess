import argon2
from dotenv import load_dotenv,get_key
load_dotenv()
import os

argon_hasher=argon2.PasswordHasher(time_cost=int( os.environ["ARGON2_TIME_COST"]),
                                   memory_cost=int(os.environ['ARGON2_MEMORYT']),
                                   parallelism=int(os.environ['ARGON2_PARALLELISM']))

def hash(password:str):
    return argon_hasher.hash(f'{password}{get_key('.env','PEPPER')}')

def verify(hash:str,password:str):
    return argon_hasher.verify(hash,f'{password}{get_key('.env','PEPPER')}')