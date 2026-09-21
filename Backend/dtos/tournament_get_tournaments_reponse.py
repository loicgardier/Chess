from pydantic import BaseModel,EmailStr,SecretStr,Field
from models.tournaments import Tournaments
from datetime import datetime,date
from repositories.tournaments_repository import TournamentsRepository
from models.tournaments import Tournaments
from repositories.users_repository import UsersRepository
from models.users import Users

class TournamentGetTournamentResponse(BaseModel):

    id:int = Field(description="Tournament id")
    nom:str = Field(description="Tournament name")
    lieu:str|None = Field(description="Tournament place")
    inscript:int = Field(description="Number of register user")
    elo_min:int = Field(description="Tournament elo min")
    elo_max:int = Field(description="Tournament elo max")
    status:Tournaments.Status = Field(description="Tournament status")
    ronde:int = Field(description="Tournament round")
    women_only:bool = Field(description="Is the tournament women only")
    date_de_fin_inscription: datetime = Field(description="Tournament date of end of registration")
    can_register:bool|None = Field(description="Can the user register",default=None)
    is_registered:bool|None = Field(description="Is the userregistered",default=None)

    def from_model(tournament_repository:TournamentsRepository,
                   user_repository:UsersRepository,
                   id:int,username:str=None):
        tournament = tournament_repository.get_one(id)
        if tournament:
            tournament_dto= TournamentGetTournamentResponse(
                id=tournament.id,
                nom=tournament.nom,
                lieu=tournament.lieu,
                elo_min=tournament.elo_min,
                elo_max=tournament.elo_max,
                status=tournament.status,
                ronde=tournament.ronde,
                women_only=tournament.women_only,
                date_de_fin_inscription=tournament.date_de_fin_inscription,
                inscript= tournament_repository.get_nb_inscript(tournament.id)
            )

            if username:
                user=user_repository.get_by_mail_or_pseudo(username)
                if user:
                    tournament_dto.can_register=tournament_repository.can_register(user.id,tournament.id)
                    tournament_dto.is_registered=tournament_repository.is_registered(user.id,tournament.id)
            return tournament_dto
