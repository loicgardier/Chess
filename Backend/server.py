from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controlers import user_controler,tournament_controler
import uvicorn
from dotenv import load_dotenv
import os

load_dotenv()

app=FastAPI()

app.add_middleware(
CORSMiddleware,
allow_origins=[os.environ['CLIENT_ORIGIN']], 
allow_credentials=True, 
allow_methods=["*"],
allow_headers=["*"],
)

app.include_router(user_controler.user_router)
app.include_router(tournament_controler.tournament_router)

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000,reload=True)