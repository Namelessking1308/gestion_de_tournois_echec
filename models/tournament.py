from enum import Enum

class Categories(Enum):
    JUNIOR = "Junior"
    SENIOR = "Senior"
    VETERAN = "Veteran"

class Type(Enum):
    FEMALE = "Women Only"
    MALE = "Male Only"
    MIXTe = "MIXTE"

class Tournament(Categories, Type):

    # region Attributs

    def __init__(self, name, location, number_of_players, elo, categories : Categories, status, current_round_number, type : Type):
        self._name = name
        self._location = location
        self.__number_of_players = number_of_players
        self.__elo = elo
        self.__categories = categories
        self._status = status
        self.__current_round_number = current_round_number
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
        if value <= 0:
            raise ValueError("The number of players must be positive.")
        self.__number_of_players = value

    @property
    def elo(self):
        return self.__elo
    
    @elo.setter
    def elo(self, value):
        value = max(0, min(value = 3000))
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
        return self._status

    @property
    def current_round_number(self):
        return self.__current_round_number
    
    @current_round_number.setter
    def current_round_number(self, value):
        if value <= 1:
            raise ValueError("The tournament must start from the first round.")
        
    @property
    def type(self):
        return self.__type
    
    @type.setter
    def type(self, value):
        if not isinstance(value, Type):
            raise ValueError("The Type must be Female/Male/Mixte")
        self.__type = value
    #endregion