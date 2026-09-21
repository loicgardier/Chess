from pydantic import BaseModel,EmailStr,SecretStr,Field
from models.tournaments import Tournaments
from datetime import datetime,date

class TournamentCreateTournamentRequest(BaseModel):

    nom:str = Field(description="Tournament name")
    lieu:str|None = Field(description="Tournament place",default=None)
    inscript_min:int = Field(description="Tournament min register",default=2)
    inscript_max:int = Field(description="Tournament min register",default=32)
    elo_min:int = Field(description="Tournament elo min",default=0)
    elo_max:int = Field(description="Tournament elo max",default=3000)
    women_only:bool = Field(description="Is the tournament women only")
    date_de_fin_inscription: date = Field(description="Tournament date of end of registration")


    def to_tournament_model(self)->Tournaments:
        tournament=Tournaments()
        tournament.nom=self.nom
        tournament.lieu=self.lieu
        tournament.inscript_min=self.inscript_min
        tournament.inscript_max=self.inscript_max
        tournament.elo_min=self.elo_min
        tournament.elo_max=self.elo_max
        tournament.status = Tournaments.Status.EnAttente
        tournament.ronde=0
        tournament.women_only=self.women_only
        tournament.date_de_fin_inscription=datetime(self.date_de_fin_inscription.year,self.date_de_fin_inscription.month,self.date_de_fin_inscription.day)
        tournament.date_de_creation=datetime.now()
        tournament.date_de_derniere_mise_a_jour=datetime.now()
        return tournament