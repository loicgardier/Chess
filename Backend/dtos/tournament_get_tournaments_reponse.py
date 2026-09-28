from pydantic import BaseModel,EmailStr,SecretStr,Field
from models.tournaments import Tournaments
from datetime import datetime,date
from repositories.tournaments_repository import TournamentsRepository
from models.tournaments import Tournaments
from repositories.users_repository import UsersRepository
from models.users import Users
from dtos.categories import Categories
from repositories.categories_repository import CategoriesRepository

class TournamentGetTournamentResponse(BaseModel):

    id:int = Field(description="Tournament id")
    nom:str = Field(description="Tournament name")
    lieu:str|None = Field(description="Tournament place")
    inscript:int = Field(description="Number of register user")
    elo_min:int = Field(description="Tournament elo min")
    elo_max:int = Field(description="Tournament elo max")
    categories:list[Categories] = Field(description="list of accepted categories",default=[])
    status:Tournaments.Status = Field(description="Tournament status")
    ronde:int = Field(description="Tournament round")
    women_only:bool = Field(description="Is the tournament women only")
    date_de_fin_inscription: datetime = Field(description="Tournament date of end of registration")
    can_register:bool|None = Field(description="Can the user register",default=None)
    is_registered:bool|None = Field(description="Is the userregistered",default=None)

    def from_model(tournament_repository:TournamentsRepository,
                   user_repository:UsersRepository,
                   category_repository:CategoriesRepository,
                   id:int,username:str=None):
        tournament = tournament_repository.get_one(id)
        if tournament:
            categories_id = category_repository.get_by_tournament(tournament.id)
            categories=[]
            for category_id in categories_id:
                categories.append(Categories(name=category_repository.get_one(category_id.id_categorie).name))
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
                inscript= tournament_repository.get_nb_inscript(tournament.id),
                categories=categories
            )

            if username:
                user=user_repository.get_by_mail_or_pseudo(username)
                if user:
                    tournament_dto.can_register=tournament_repository.can_register(user.id,tournament.id)
                    tournament_dto.is_registered=tournament_repository.is_registered(user.id,tournament.id)
            return tournament_dto
