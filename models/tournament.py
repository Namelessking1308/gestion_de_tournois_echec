class Tournament:

    # region Attributs
    
    def __init__(self, name, location, number_of_player, elo, categories, status, current_round_number, type):
        self.name = name
        self.location = location
        self.number_of_player = number_of_player
        self.elo = elo
        self.categories = categories
        self.status = status
        self.current_roun_number = current_round_number
        self.type = type

    #endregion