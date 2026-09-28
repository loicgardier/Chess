from pydantic import Field,BaseModel


class UserConnectionReponse(BaseModel):
    token:str =Field(description="bearer token",default='')