

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
            "║" + f"  {'#':<4} {'Player':<18} {'Played':>6} {'Wins':>5} {'Draws':>6} {'Losses':>7} {'Score':>6}" + "║",
            "╠" + "─" * w + "╣",
        ]

        for rank, s in enumerate(standings, start=1):
            medal = medals.get(rank, f"  {rank}.")
            name  = s['player'].username
            lines.append(
                "║" +
                f"  {medal:<4} {name:<18} {s['played']:>6} {s['wins']:>5}"
                f"{s['draws']:>6} {s['losses']:>7} {s['score']:>6.1f}" +
                "║"
            )

        lines += [
            "╚" + "═" * w + "╝",
            ""
        ]

        return "\n".join(lines)

    #endregion
