from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(os.environ["DATABASE_CONEXION_STRING"], echo=True)
session_maker = sessionmaker(bind=engine)

def get_session():
    try:
        session = session_maker()
        yield session
    except:
        raise
    finally:
        session.close()