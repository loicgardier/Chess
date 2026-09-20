from fastapi import FastAPI
from controlers import user_controler,tournament_controler
import uvicorn

app=FastAPI()
app.include_router(user_controler.user_router)
app.include_router(tournament_controler.tournament_router)

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000,reload=True)