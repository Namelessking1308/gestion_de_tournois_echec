from models import Player, Tournament, Gender, Status, Categories, Type

def main():

   player1 = Player(
    "Bob",
    "bob@gmail.com",
    "19/08/1999",
    Gender.MALE.value,
    "01/01/2026",
    2100
)

   tournament1 = Tournament("Mondial", 
                            "Spain", 
                            2, 
                            1800, 
                            Categories.JUNIOR.value,
                            Type.MIXTE.value, 
                            "17/02/2026"
)

   print(player1.display())

   print()

   print(tournament1.add_player(player1))

   print()

   tournament1.check_registration(player1)

   print()

   print(tournament1.add_tournament())

   print()

   print(tournament1.remove_tournament())

   print()

   print(tournament1.display_tournament())



if __name__ == "__main__":
    main()