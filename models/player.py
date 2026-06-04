from enum import Enum
from models import Tournament
class Gender(Enum):
    FEMALE = "Female"
    MALE = "Male"


class Player:

    #region attributs

    def __init__(self, username, email, date_of_birth, gendre : Gender, registration_date, elo = 1200):
        self.__username = username
        self.__email = email
        self.__date_of_birth = date_of_birth
        self.__gendre = gendre
        self.__registration_date = registration_date
        self.__elo = max(0, min(elo, 3000))

    #endregion

    #region Prop's

    @property
    def username(self):
        return self.__username
    
    @username.setter
    def username(self, value):
        self.__username = value

    @property
    def email(self):
        return self.__email
    
    @email.setter
    def email(self, value):
        import re

        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        if not re.match(pattern, value):
            raise ValueError("Invalid email format")

        self.__email = value

    @property
    def date_of_birth(self):
        return self.__date_of_birth

    @property
    def age(self):
        from datetime import datetime

        try:
            birth_date = datetime.strptime(self.__date_of_birth, "%d/%m/%Y")
        except ValueError:
            raise ValueError("Invalid birth date format (DD/MM/YYYY expected)")

        today = datetime.today()

        age = today.year - birth_date.year

        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1

        return age
    
    @property
    def gender(self):
        return self.__gendre
    
    @gender.setter
    def gender(self, value):
        if not isinstance(value, Gender):
            raise ValueError("The gender must be Male or Female")
        self.__gendre = value

    @property
    def registration_date(self):
        pass

    @property
    def elo(self):
        return self.__elo
    
    @elo.setter
    def elo(self, value):
        if value < 1200 or value > 3000:
            raise ValueError("The ELO must be bewteen 1200 and 3000")
        self.__elo = value

    #endregion