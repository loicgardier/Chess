from pydantic import Field,BaseModel


class UserInscriptionReponse(BaseModel):
    token:str =Field(description="bearer token")
