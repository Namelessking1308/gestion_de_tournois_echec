class Player:

    #region attributs

    def __init__(self, username, email, date_of_birth, gendre, elo = 1200):
        self.username = username
        self.email = email
        self.date_of_birth = date_of_birth
        self.gendre = gendre
        self.elo = max(0, min(elo, 3000))

    #endregion