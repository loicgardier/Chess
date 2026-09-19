from fastapi import FastAPI
from controlers import user_controler
import uvicorn

app=FastAPI()
app.include_router(user_controler.user_router)

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000,reload=True)