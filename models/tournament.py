from enum import Enum

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

class Tournament(Categories, Type, Status):

    # region Attributs

    def __init__(self, name, location, number_of_players, elo, categories : Categories, status : Status, type : Type):
        self._name = name
        self._location = location
        self.__number_of_players = number_of_players
        self.__elo = elo
        self.__categories = categories
        self.__status = status.self.WAITING
        self.__current_round_number = 0
        self.__type = type

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
        if value < 1200 or value > 3000:
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

    #endregion

    #region Méthodes

    

    #endregion