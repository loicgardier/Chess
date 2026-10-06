from pydantic import BaseModel,Field,computed_field


class LeaderboardResponse(BaseModel):
    pseudo:str = Field(description="User pseudo")
    victoire:int = Field(description="Number of victory",default=0)
    equalite:int = Field(description="Number of equality",default=0)
    defaite:int = Field(description="Number of defeat",default=0)

    @computed_field
    @property
    def match_played(self)->int:
        return self.victoire+self.equalite+self.defaite

    @computed_field
    @property
    def points(self)->float:
        return self.victoire+(self.equalite/2)