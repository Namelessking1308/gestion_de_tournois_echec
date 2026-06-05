from models import Player, Tournament, Gender, Status, Categories, Type, Match_result, Leaderboard


def main():

    # ── Création des joueurs ────────────────────────────────────────────────
    player1 = Player(
        "Bob",
        "bob@gmail.com",
        "19/08/1965",
        Gender.MALE.value,
        "01/01/2026",
        2100
    )

    player2 = Player(
        "Alice",
        "alice@gmail.com",
        "12/04/1990",
        Gender.FEMALE.value,
        "01/01/2026",
        1900
    )

    # ── Création du tournoi ─────────────────────────────────────────────────
    tournament1 = Tournament(
        "Mondial",
        "Spain",
        4,
        1800,
        Categories.SENIOR.value,
        Type.MIXTE.value,
        "17/02/2026"
    )

    # ── Infos basiques ──────────────────────────────────────────────────────
    print(f"Age of {player1.username} : {player1.age}")

    print(tournament1.add_tournament())
    print(tournament1.change_status(Status.WAITING.value))
    print(tournament1.remove_tournament())
    print(tournament1.display_tournament())

    # ── Inscription des joueurs ─────────────────────────────────────────────
    print(tournament1.add_player(player1))
    print(tournament1.add_player(player2))

    tournament1.check_registration(player1)

    # ── Démarrage du tournoi ────────────────────────────────────────────────
    print(tournament1.start_tournament())

    # ── Affichage du round courant ──────────────────────────────────────────
    print(tournament1.display_round())

    # ── Saisie du résultat du match 0 (round courant uniquement) ───────────
    match = tournament1.match_list[0]
    match.set_result(Match_result.WHITE_PLAYER)

    print(tournament1.display_round())

    # ── Passage au round suivant ────────────────────────────────────────────
    print(tournament1.next_round())

    # ── Classement final ────────────────────────────────────────────────────
    print(Leaderboard.display(tournament1))


if __name__ == "__main__":
    main()
