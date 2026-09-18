import argon2
from dotenv import load_dotenv,get_key
load_dotenv()

argon_hasher=argon2.PasswordHasher(time_cost=get_key('.env','ARGON2_TIME_COST'),
                                   memory_cost=get_key('.env','ARGON2_MEMORYT'),
                                   parallelism=get_key('.env','ARGON2_PARALLELISM'))

def hash(password:str):
    return argon_hasher.hash(f'{password}{get_key('.env','PEPPER')}')

def verify(hash:str,password:str):
    return argon_hasher.verify(hash,f'{password}{get_key('.env','PEPPER')}')