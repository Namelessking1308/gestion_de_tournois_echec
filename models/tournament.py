from enum import Enum
from datetime import datetime

    #region Enum

class Categories(Enum):
    """Age categories available for a tournament."""
    JUNIOR  = "Junior"
    SENIOR  = "Senior"
    VETERAN = "Veteran"

class Type(Enum):
    """Gender types available for a tournament."""
    FEMALE = "Women Only"
    MALE   = "Male Only"
    MIXTE  = "Mixte"

class Status(Enum):
    """Lifecycle statuses of a tournament."""
    WAITING   = "Waiting for players..."
    PROGRESS  = "In progress"
    COMPLETED = "Completed !"

    #endregion


class Tournament:
    """
    Represents a chess tournament.

    Handles player registration, match generation (Double Round Robin),
    round progression, and status management.

    Attributes:
        name                  : Tournament name.
        location              : City / country where it takes place.
        number_of_players     : Maximum number of participants allowed.
        elo                   : Minimum ELO rating required to join.
        categories            : Age category (Junior / Senior / Veteran).
        type                  : Gender type (Male / Female / Mixte).
        registration_deadline : Last date to register (DD/MM/YYYY).
        status                : Current lifecycle status.
        current_round_number  : Active round (0 = not started).
        tournament_list       : Players currently registered.
        match_list            : All generated matches.
        all_tournament        : Class-level list of all tournaments added.
    """

    #region Attributs

    def __init__(self, name, location, number_of_players, elo,
                 categories: Categories, type: Type, registration_deadline):
        self._name                    = name
        self._location                = location
        self.__number_of_players      = number_of_players
        self.__elo                    = elo
        self.__categories             = categories
        self.__status                 = Status.WAITING.value
        self.__current_round_number   = 0
        self.__type                   = type
        self.__registration_deadline  = registration_deadline
        self.__tournament_list        = []   # Registered players
        self.__all_tournament         = []   # All tournaments (global list)
        self.__match_list             = []   # Generated matches

    #endregion

    #region Prop's

    @property
    def name(self):
        """Tournament name."""
        return self._name

    @property
    def location(self):
        """Location of the tournament."""
        return self._location

    @property
    def number_of_players(self):
        """Maximum number of players allowed."""
        return self.__number_of_players

    @number_of_players.setter
    def number_of_players(self, value):
        """Validate that player count is between 2 and 32."""
        if value < 2 or value > 32:
            raise ValueError("The number of players must be positive or min 2 max 32")
        self.__number_of_players = value

    @property
    def elo(self):
        """Minimum ELO required to participate."""
        return self.__elo

    @elo.setter
    def elo(self, value):
        """Validate ELO is between 0 and 3000."""
        if value < 0 or value > 3000:
            raise ValueError("The ELO must be between 0 and 3000")
        self.__elo = value

    @property
    def categories(self):
        """Age category of the tournament."""
        return self.__categories

    @categories.setter
    def categories(self, value):
        """Validate that category is a Categories enum member."""
        if not isinstance(value, Categories):
            raise ValueError("The Categories must be Junior/Senior/Veteran")
        self.__categories = value

    @property
    def status(self):
        """Current status of the tournament."""
        return self.__status

    @status.setter
    def status(self, value):
        """Validate that status is a Status enum member."""
        if not isinstance(value, Status):
            raise ValueError("The Status must be waiting/progress/Completed")
        self.__status = value

    @property
    def current_round_number(self):
        """Currently active round number (0 = not started)."""
        return self.__current_round_number

    @current_round_number.setter
    def current_round_number(self, value):
        """Validate that round number is not negative."""
        if value < 0:
            raise ValueError("The round number cannot be negative.")
        self.__current_round_number = value

    @property
    def type(self):
        """Gender type of the tournament."""
        return self.__type

    @type.setter
    def type(self, value):
        """Validate that type is a Type enum member."""
        if not isinstance(value, Type):
            raise ValueError("The Type must be Female/Male/Mixte")
        self.__type = value

    @property
    def registration_deadline(self):
        """Last date to register (string DD/MM/YYYY)."""
        return self.__registration_deadline

    @registration_deadline.setter
    def registration_deadline(self, value):
        """Validate date format before updating."""
        try:
            datetime.strptime(value, "%d/%m/%Y")
        except ValueError:
            raise ValueError("Invalid registration deadline (DD/MM/YYYY expected)")
        self.__registration_deadline = value

    @property
    def tournament_list(self):
        """List of registered players."""
        return self.__tournament_list

    @property
    def all_tournament(self):
        """Global list of all tournaments that have been added."""
        return self.__all_tournament

    @property
    def match_list(self):
        """List of all matches generated for this tournament."""
        return self.__match_list

    #endregion

    #region Méthodes

    def display_tournament(self):
        """
        Return a formatted string with the full details of the tournament.
        Only displayed if the tournament is not yet completed.
        """
        if self.__status is not Status.COMPLETED:
            w = 50
            lines = [
                "",
                "╔" + "═" * w + " ╗",
                "║" + f"  ♟  TOURNAMENT : {self._name}".center(w) + " ║",
                "╠" + "═" * w + " ╣",
                "║" + f"  📍 Location      : {self._location}".ljust(w) + "║",
                "║" + f"  👥 Max players   : {self.__number_of_players}".ljust(w) + "║",
                "║" + f"  ⚡ Min ELO       : {self.__elo}".ljust(w) + "║",
                "║" + f"  🏷  Category      : {self.__categories}".ljust(w) + " ║",
                "║" + f"  🚻 Type          : {self.__type}".ljust(w) + "║",
                "║" + f"  📌 Status        : {self.__status}".ljust(w) + "║",
                "║" + f"  📅 Deadline      : {self.__registration_deadline}".ljust(w) + "║",
                "║" + f"  🔁 Current round : {self.__current_round_number}".ljust(w) + "║",
                "╚" + "═" * w + " ╝",
                ""
            ]
            return "\n".join(lines)

    def remove_tournament(self):
        """
        Remove this tournament from the global list.
        Only possible when status is WAITING.
        """
        if self.status == Status.WAITING.value:
            self.all_tournament.remove(self)
            return f"The tournament {self.name} has been successfully deleted !"
        else:
            return f"A tournament can only be deleted if the status is Waiting..."

    def is_registration_valid(self, player):
        """
        Check if a player's registration date is on or before the deadline.
        Returns True if registration is valid, False otherwise.
        """
        registration_date = datetime.strptime(player.registration_date, "%d/%m/%Y")
        deadline          = datetime.strptime(self.__registration_deadline, "%d/%m/%Y")
        return registration_date <= deadline

    def check_registration(self, player):
        """
        Print whether a player's registration date is valid or too late.
        """
        if self.is_registration_valid(player):
            print("Registration is valid !")
        else:
            print("Registration is too late...")

    def add_player(self, player):
        """
        Attempt to register a player into the tournament.

        Checks (in order):
          1. Tournament is not full.
          2. Player is not already registered.
          3. Tournament status is WAITING.
          4. Player age is between 18 and 60.
          5. Player ELO meets the minimum requirement.
          6. Player gender matches the tournament type (unless MIXTE).
        """
        if len(self.tournament_list) >= self.number_of_players:
            return f"Maximum capacity reached ({self.number_of_players})"

        if player in self.__tournament_list:
            return f"{player.username} is already in the tournament"

        if self.__status == Status.PROGRESS.value:
            return f"You can't join the tournament because the status is {Status.PROGRESS.value}"

        if self.__status == Status.COMPLETED.value:
            return f"You can't join the tournament because the status is {Status.COMPLETED.value}"

        if player.age < 18 or player.age > 60:
            return f"You don't have the age to join this tournament"

        if player.elo < self.elo:
            return f"You don't have the elo to join this tournament"

        if self.__type != Type.MIXTE.value and player.gender != self.__type:
            return f"This tournament is {self.__type} only."

        self.tournament_list.append(player)
        return f"{player.username} added to {self.name}"

    def add_tournament(self):
        """
        Add this tournament to the global all_tournament list.
        """
        self.all_tournament.append(self)
        return f"The tournament {self.name} has been added to the list of tournament !"

    def change_status(self, status):
        """
        Manually override the tournament status.
        Used for admin/testing purposes.
        """
        self.__status = status
        return status

    def start_tournament(self):
        """
        Start the tournament.

        Business rules:
          - Registration deadline must have passed.
          - At least 2 players must be registered.

        On success:
          - Status set to PROGRESS.
          - current_round_number set to 1.
          - All Double Round Robin matches generated and stored in match_list.
        """
        try:
            from .match import Match
        except ImportError:
            from models.match import Match

        today    = datetime.today()
        deadline = datetime.strptime(self.__registration_deadline, "%d/%m/%Y")

        if today < deadline:
            return f"The registration deadline has not passed yet ({self.__registration_deadline})."

        if len(self.__tournament_list) < 2:
            return f"Not enough players to start the tournament (minimum 2)."

        self.__status               = Status.PROGRESS.value
        self.__current_round_number = 1
        self.__match_list           = Match.generate_round_robin_double(self)

        return f"The tournament {self._name} has started ! Round 1 begins."

    def next_round(self):
        """
        Advance to the next round.

        Rules:
          - All matches of the current round must be played first.
          - If this was the last round, the tournament is marked as COMPLETED.
          - Otherwise, current_round_number is incremented by 1.
        """
        current_matches = [m for m in self.__match_list
                           if m.round_number == self.__current_round_number]

        unplayed = [m for m in current_matches if not m.is_played]

        if unplayed:
            return (f"Cannot move to the next round : "
                    f"{len(unplayed)} match(es) of round {self.__current_round_number} "
                    f"have not been played yet.")

        total_rounds = max((m.round_number for m in self.__match_list), default=0)

        if self.__current_round_number >= total_rounds:
            self.__status = Status.COMPLETED.value
            return f"All rounds are completed ! The tournament {self._name} is over."

        self.__current_round_number += 1
        return f"Round {self.__current_round_number} begins !"

    def display_round(self, round_number=None):
        """
        Return a formatted string showing all matches of a given round.
        Defaults to the current round if no round_number is provided.
        """
        r       = round_number if round_number is not None else self.__current_round_number
        matches = [m for m in self.__match_list if m.round_number == r]
        w       = 58

        lines = [
            "",
            "╔" + "═" * w + "╗",
            "║" + f"  ♟  {self._name}  —  ROUND {r}".center(w) + "║",
            "╠" + "─" * w + "╣",
        ]

        for m in matches:
            lines.append("║  " + m.display().replace("\n", "\n║  ") + "║")
            lines.append("║" + " " * w + "║")

        played   = sum(1 for m in matches if m.is_played)
        total    = len(matches)
        lines += [
            "╠" + "─" * w + "╣",
            "║" + f"  Played : {played} / {total}".ljust(w) + "║",
            "╚" + "═" * w + "╝",
            ""
        ]

        return "\n".join(lines)

    #endregion
