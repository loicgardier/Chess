from pydantic import BaseModel,EmailStr,SecretStr,Field
from models.users import Users

class UserConnectionRequest(BaseModel):

    pseudo_or_mail:str|EmailStr =Field(description="User pseudo or password")
    password:SecretStr =Field(description="User password")
