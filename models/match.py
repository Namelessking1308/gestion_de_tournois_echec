from enum import Enum
import itertools
import uuid


    #region Enum

class Match_result(Enum):
    """Enumeration of all possible results for a chess match."""
    NOT_PLAYED   = "Not played"
    WHITE_PLAYER = "White player"
    BLACK_PLAYER = "Black player"
    DRAW         = "Draw"

    #endregion


class Match:
    """
    Represents a single chess match between two players inside a tournament.

    Attributes:
        id             : Unique identifier auto-generated with uuid.
        tournament_id  : Name/ID of the parent tournament.
        white_player   : Player object assigned to the white pieces.
        black_player   : Player object assigned to the black pieces.
        round_number   : The round this match belongs to.
        result         : Current result (default NOT_PLAYED).
        tournament     : Reference to the parent Tournament (injected after creation).
    """

    #region Attributs

    def __init__(self, tournament_id, white_player, black_player, round_number):
        self.__id             = str(uuid.uuid4())[:8]
        self.__tournament_id  = tournament_id
        self.__white_player   = white_player
        self.__black_player   = black_player
        self.__round_number   = round_number
        self.__result         = Match_result.NOT_PLAYED
        self.__tournament     = None   # Injected by Tournament.start_tournament()

    #endregion

    #region Prop's

    @property
    def id(self):
        """Unique identifier of this match."""
        return self.__id

    @property
    def tournament_id(self):
        """Name or ID of the parent tournament."""
        return self.__tournament_id

    @property
    def white_player(self):
        """Player assigned to white pieces."""
        return self.__white_player

    @property
    def black_player(self):
        """Player assigned to black pieces."""
        return self.__black_player

    @property
    def round_number(self):
        """Round number this match belongs to."""
        return self.__round_number

    @property
    def result(self):
        """Current result of the match (Match_result enum)."""
        return self.__result

    @property
    def tournament(self):
        """Reference to the parent Tournament object."""
        return self.__tournament

    @tournament.setter
    def tournament(self, value):
        """Inject the parent tournament reference after match creation."""
        self.__tournament = value

    @property
    def is_played(self):
        """Returns True if the match has a result other than NOT_PLAYED."""
        return self.__result != Match_result.NOT_PLAYED

    #endregion

    #region Méthodes

    def set_result(self, result: Match_result):
        """
        Set the result of the match.
        Rules:
          - Result must be a valid Match_result value.
          - Cannot set result to NOT_PLAYED (use reset_result() instead).
          - Can only modify if this match belongs to the current round of the tournament.
        """
        if not isinstance(result, Match_result):
            raise ValueError("Result must be a Match_result value.")

        if result == Match_result.NOT_PLAYED:
            raise ValueError("Use reset_result() to set a match back to Not played.")

        if self.__tournament is not None:
            if self.__round_number != self.__tournament.current_round_number:
                raise ValueError(
                    f"Cannot modify match from round {self.__round_number}. "
                    f"Current round is {self.__tournament.current_round_number}."
                )

        self.__result = result

    def reset_result(self):
        """
        Reset the match result back to NOT_PLAYED.
        Can only be done on matches belonging to the current round.
        """
        if self.__tournament is not None:
            if self.__round_number != self.__tournament.current_round_number:
                raise ValueError(
                    f"Cannot reset match from round {self.__round_number}. "
                    f"Current round is {self.__tournament.current_round_number}."
                )
        self.__result = Match_result.NOT_PLAYED

    def get_points_for(self, player):
        """
        Return the points earned by a given player for this match.
        Win = 1.0 | Draw = 0.5 | Loss = 0.0 | Not played = 0.0
        """
        if not self.is_played:
            return 0.0

        if player == self.__white_player:
            if self.__result == Match_result.WHITE_PLAYER:
                return 1.0
            elif self.__result == Match_result.DRAW:
                return 0.5
            else:
                return 0.0

        if player == self.__black_player:
            if self.__result == Match_result.BLACK_PLAYER:
                return 1.0
            elif self.__result == Match_result.DRAW:
                return 0.5
            else:
                return 0.0

        return 0.0

    def display(self):
        """Return a formatted string showing all details of this match."""
        w = self.__white_player.username
        b = self.__black_player.username
        res = self.__result.value

        w_tag = " <<" if self.__result == Match_result.WHITE_PLAYER else ""
        b_tag = " <<" if self.__result == Match_result.BLACK_PLAYER else ""
        draw  = "  [ DRAW ]" if self.__result == Match_result.DRAW else ""
        played_tag = "[ NOT PLAYED ]" if not self.is_played else ""

        return (f"  Match #{self.__id}  |  Round {self.__round_number}\n"
                f"  ♔ {w:<20}{w_tag}  vs  ♚ {b:<20}{b_tag}{draw}  {played_tag}")

    #endregion

    #region Static methods

    @staticmethod
    def generate_round_robin_double(tournament):
        """
        Generate all matches for a Double Round Robin tournament.

        Algorithm:
          - Build every unique pair (A, B) from the player list.
          - First half  : A plays White, B plays Black  → rounds 1..N
          - Second half : B plays White, A plays Black  → rounds N+1..2N
          - The parent tournament reference is injected into every match.

        Returns a list of Match objects ready to use.
        """
        players = tournament.tournament_list
        pairs   = list(itertools.combinations(players, 2))
        half    = len(pairs)
        matches = []

        # First half : A White, B Black
        for round_number, (player_a, player_b) in enumerate(pairs, start=1):
            match = Match(tournament.name, player_a, player_b, round_number)
            match.tournament = tournament
            matches.append(match)

        # Second half : colours reversed
        for round_number, (player_a, player_b) in enumerate(pairs, start=half + 1):
            match = Match(tournament.name, player_b, player_a, round_number)
            match.tournament = tournament
            matches.append(match)

        return matches

    #endregion


class Leaderboard:
    """
    Computes and displays the ranking for a tournament.

    Scoring rules:
      Win  = 1 point
      Draw = 0.5 points
      Loss = 0 points

    Ranking is sorted by descending score, then by number of wins.
    """

    #region Static methods

    @staticmethod
    def get_standings(tournament):
        """
        Compute statistics for every registered player in the tournament.

        Iterates over all played matches and accumulates:
          played, wins, draws, losses, score.

        Returns a list of dicts sorted by score (desc) then wins (desc).
        """
        stats = {}

        for player in tournament.tournament_list:
            stats[player.username] = {
                "player":  player,
                "played":  0,
                "wins":    0,
                "draws":   0,
                "losses":  0,
                "score":   0.0
            }

        for match in tournament.match_list:
            if not match.is_played:
                continue

            for player in (match.white_player, match.black_player):
                points = match.get_points_for(player)
                s = stats[player.username]
                s["played"] += 1
                s["score"]  += points

                if points == 1.0:
                    s["wins"]   += 1
                elif points == 0.5:
                    s["draws"]  += 1
                else:
                    s["losses"] += 1

        return sorted(
            stats.values(),
            key=lambda x: (-x["score"], -x["wins"])
        )

    @staticmethod
    def display(tournament):
        """
        Build and return a formatted leaderboard string for the given tournament.
        Columns : Rank | Player | Played | Wins | Draws | Losses | Score
        """
        standings = Leaderboard.get_standings(tournament)
        w = 58
        medals = {1: "🥇", 2: "🥈", 3: "🥉"}

        lines = [
            "",
            "╔" + "═" * w + "╗",
            "║" + f"  🏆  LEADERBOARD : {tournament.name}".center(w) + "║",
            "║" + f"  Round {tournament.current_round_number}".center(w) + "║",
            "╠" + "═" * w + "╣",
            "║" + f"  {'#':<4} {'Player':<18} {'Played':>6} {'Wins':>5} {'Draws':>6} {'Losses':>7} {'Score':>6}  " + "║",
            "╠" + "─" * w + "╣",
        ]

        for rank, s in enumerate(standings, start=1):
            medal = medals.get(rank, f"  {rank}.")
            name  = s['player'].username
            lines.append(
                "║" +
                f"  {medal:<4} {name:<18} {s['played']:>6} {s['wins']:>5} "
                f"{s['draws']:>6} {s['losses']:>7} {s['score']:>6.1f}  " +
                "║"
            )

        lines += [
            "╚" + "═" * w + "╝",
            ""
        ]

        return "\n".join(lines)

    #endregion
