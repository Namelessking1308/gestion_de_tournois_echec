from enum import Enum
from datetime import datetime
# from .player import Player

    #region Enum

class Categories(Enum):
    JUNIOR = "Junior"
    SENIOR = "Senior"
    VETERAN = "Veteran"

class Type(Enum):
    FEMALE = "Women Only"
    MALE = "Male Only"
    MIXTE = "Mixte"

class Status(Enum):
    WAITING = "Waiting for players..."
    PROGRESS = "In progress"
    COMPLETED = "Completed !"

    #endregion

class Tournament:

    # region Attributs

    def __init__(self, name, location, number_of_players, elo, categories : Categories, type : Type, registration_deadline):
        self._name = name
        self._location = location
        self.__number_of_players = number_of_players
        self.__elo = elo
        self.__categories = categories
        self.__status = Status.WAITING.value
        self.__current_round_number = 0
        self.__type = type
        self.__registration_deadline = registration_deadline
        self.__tournament_list = []
        self.__all_tournament = []

    #endregion

    #region Prop's

    @property
    def name(self):
        return self._name
    
    @property
    def location(self):
        return self._location
    
    @property
    def number_of_players(self):
        return self.__number_of_players
    
    @number_of_players.setter
    def number_of_players(self, value):
        if value < 2 or value > 32:
            raise ValueError("The number of players must be positive or min 2 max 32")
        self.__number_of_players = value

    @property
    def elo(self):
        return self.__elo
    
    @elo.setter
    def elo(self, value):
        if value < 0 or value > 3000:
            raise ValueError("The ELO must be bewteen 1200 and 3000")
        self.__elo = value

    @property
    def categories(self):
        return self.__categories
    
    @categories.setter
    def categories(self, value):
        if not isinstance(value, Categories):
            raise ValueError("The Categories must be Junior/Senior/Veteran")
        self.__categories = value

    @property
    def status(self):
        return self.__status
    
    @status.setter
    def status(self, value):
        if not isinstance(value, Status):
            raise ValueError("The Status must be waiting/progress/Completed")
        self.__status = value

    @property
    def current_round_number(self):
        return self.__current_round_number
    
    @current_round_number.setter
    def current_round_number(self, value):
        if value < 0:
            raise ValueError("The round number cannot be negative.")
        self.__current_round_number = value
        
    @property
    def type(self):
        return self.__type
    
    @type.setter
    def type(self, value):
        if not isinstance(value, Type):
            raise ValueError("The Type must be Female/Male/Mixte")
        self.__type = value

    @property
    def registration_deadline(self):
        return self.__registration_deadline
    
    @registration_deadline.setter
    def registration_deadline(self, value):
        try:
            datetime.strptime(self.__registration_deadline, "%d/%m/%Y")
        except ValueError:
            raise ValueError("Invalid registration deadline (DD/MM/YYYY expected)")
        self.__registration_deadline = value

    @property
    def tournament_list(self):
            return self.__tournament_list

    @property
    def all_tournament(self):
        return self.__all_tournament
    

    #endregion

    #region Méthodes

    def display_tournament(self):
        if self.__status is not Status.COMPLETED:
            return (f"--TOURNAMENT--\n"
                    f"\n{self._name}\n"
                    f"\n--LOCATION--\n"
                    f"\n{self._location}\n"
                    f"\nNUMBER OF PLAYERS: {self.__number_of_players}\n"
                    f"\nMinimum 2 players / MAX {self.__number_of_players} players\n"
                    f"\n--CATEGORIE--\n"
                    f"\n{self.__categories}\n"
                    f"\n--ELO--\n"
                    f"\nMin 1200 MAX {self.__elo}\n"
                    f"\n--STATUS--\n"
                    f"\n{self.__status}\n"
                    f"\n--Last date of registration--\n"
                    f"\n{self.__registration_deadline}\n"
                    f"\n--Current round--\n"
                    f"\n{self.__current_round_number}")

    def remove_tournament(self):
        if self.status == Status.WAITING.value:
            self.all_tournament.remove(self)
            return f"The tournament {self.name} has been successfully deleted !"
        else:
            return f"A tournament can only be deleted if the status is Waiting..."

    def is_registration_valid(self, player):
        registration_date = datetime.strptime(player.registration_date, "%d/%m/%Y")

        deadline = datetime.strptime(self.__registration_deadline, "%d/%m/%Y")

        return registration_date <= deadline

    def check_registration(self, player):
        if self.is_registration_valid(player):
            print("Registration is valide !")
        else:
            print("Registration is too late...")

    def add_player(self, player):
        if not hasattr(self, 'tournament_list'):
            self.__tournament_list = []

        if len(self.tournament_list) >= self.number_of_players:
            return f"Maximum capacity reached ({self.number_of_players})"
        elif player in self.__tournament_list:
            return f"{player.username} is already in the tournament"
        elif self.__status == Status.PROGRESS.value:
            return f"You can't join the tournament because the status is {Status.PROGRESS.value}"
        elif self.__status == Status.COMPLETED.value:
            return f"You can't join the tournament because the status is {Status.COMPLETED.value}"
        elif player.age < 18:
            return f"You don't have the age to join this tournament"
        elif player.age < 18 and player.age > 60:
            return f"You don't have the age to join this tournament"
        elif player.age > 60:
            return f"You don't have the age to join this tournament"
        elif player.elo < self.elo:
            return f"You don't have the elo to join this tournament"
        elif player.gender != self.__type:
            return f"This tournament is {self.__type} only."

        self.tournament_list.append(player)

        return f"{player.username} added to {self.name}"

    def add_tournament(self):
        if not hasattr(self, 'all_tournament'):
            self.__all_tournament = []

        self.all_tournament.append(self)

        return f"The tournament {self.name} has been added to the list of tournament !"

    def change_status(self, status):
        self.__status = status
        return status

    #endregion