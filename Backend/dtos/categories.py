from pydantic import Field,BaseModel

class Categories(BaseModel):
    name:str =Field(description="Category name",default='')