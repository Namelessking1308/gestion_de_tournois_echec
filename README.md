# ♟ Chess Tournament Management

A Python application for managing chess tournaments using a Double Round Robin format.

---

## Project Structure

```
GESTION_DE_TOURNOIS_ECHEC/
│
├── main.py                  # Entry point
│
└── models/
    ├── __init__.py          # Exports all classes
    ├── player.py            # Player class
    ├── tournament.py        # Tournament class + enums
    ├── match.py             # Match class
    └── Leaderboard.py       # Leaderboard class
```

---

## Getting Started

**Requirements:** Python 3.10+, no external dependencies.

```bash
# Clone the project
git clone <https://github.com/Namelessking1308/gestion_de_tournois_echec>
cd GESTION_DE_TOURNOIS_ECHEC

# Run the application
python main.py
```

---

## Features & Specifications

### 1. Player Management

A player has the following attributes:

| Field | Type | Rules |
|---|---|---|
| Username | `str` | Required |
| Email | `str` | Must be a valid email format |
| Date of birth | `str` | Format `DD/MM/YYYY` |
| Gender | `Gender` enum | `Male`, `Female`, `Mixte` |
| Registration date | `str` | Format `DD/MM/YYYY` |
| ELO | `int` | Between `0` and `3000` — defaults to `1200` if not provided |

**Business rule:** If a player has no ELO rating, they start at **1200** by default.

```python
player = Player("Alice", "alice@gmail.com", "12/04/1990", Gender.FEMALE.value, "01/01/2026", 1900)
print(player.age)     # Computed from date of birth
print(player.display())
```

---

### 2. Tournament Management

A tournament has the following attributes:

| Field | Type | Rules |
|---|---|---|
| Name | `str` | Required |
| Location | `str` | Required |
| Number of players | `int` | Between `2` and `32` |
| ELO | `int` | Minimum ELO required to join (`0`–`3000`) |
| Category | `Categories` enum | `Junior`, `Senior`, `Veteran` |
| Type | `Type` enum | `Male Only`, `Women Only`, `Mixte` |
| Registration deadline | `str` | Format `DD/MM/YYYY` |
| Status | `Status` enum | `Waiting`, `In progress`, `Completed` |
| Current round | `int` | Starts at `0`, moves to `1` on start |

**Business rules on creation:**
- Current round is `0` and status is `Waiting for players` upon creation.
- Minimum number of players must be ≤ maximum number of players.

```python
tournament = Tournament("Mondial", "Spain", 4, 1800, Categories.SENIOR.value, Type.MIXTE.value, "17/02/2026")
print(tournament.add_tournament())
print(tournament.display_tournament())
```

**Delete a tournament:**
A tournament can only be deleted if its status is still `Waiting`.

```python
print(tournament.remove_tournament())
```

---

### 3. Display & Consultation

**Tournament details** — displays name, location, player count, ELO range, category, type, status, deadline and current round.

```python
print(tournament.display_tournament())
```

**Round display** — shows all matches for a given round and how many have been played.

```python
print(tournament.display_round())           # Current round
print(tournament.display_round(round_number=2))  # Specific round
```

---

### 4. Registrations & Cancellations

**Add a player** — `tournament.add_player(player)`

All of the following conditions must be met:

| Condition | Detail |
|---|---|
| Tournament not started | Status must be `Waiting` |
| Deadline not passed | Player's registration date ≤ tournament deadline |
| Not already registered | Player must not be in the tournament list |
| Capacity not reached | Current registrants < max players |
| Age | Junior: < 18 · Senior: ≥ 18 and < 60 · Veteran: ≥ 60 |
| ELO | Player ELO ≥ tournament minimum ELO |
| Gender | If `Women Only`, only `Female` and `Other` are accepted |

```python
print(tournament.add_player(player1))
tournament.check_registration(player1)   # Checks deadline validity
```

---

### 5. Tournament Progression

#### Start a tournament

```python
print(tournament.start_tournament())
```

**Business rules:**
- Registration deadline must have passed.
- At least **2 players** must be registered.
- On success: status → `In progress`, current round → `1`.
- All matches are automatically generated using **Double Round Robin**.

#### Match generation — Double Round Robin

Each player meets every other player **twice**: once as White, once as Black.

For `N` players, the total number of matches is `N × (N - 1)`.

A match contains:

| Field | Detail |
|---|---|
| ID | Auto-generated (UUID) |
| Tournament ID | Name of the parent tournament |
| White player | `Player` object |
| Black player | `Player` object |
| Round number | Which round this match belongs to |
| Result | `Not played` · `White player` · `Black player` · `Draw` |

#### Set a match result

```python
match = tournament.match_list[0]
match.set_result(Match_result.WHITE_PLAYER)   # White wins
match.set_result(Match_result.BLACK_PLAYER)   # Black wins
match.set_result(Match_result.DRAW)           # Draw
match.reset_result()                          # Back to Not played
```

**Business rule:** A result can only be set or modified if the match belongs to the **current round**.

#### Move to the next round

```python
print(tournament.next_round())
```

**Business rules:**
- All matches of the current round must be played first.
- If it was the last round, the tournament is marked as `Completed`.

---

### 6. Rankings & Scores

```python
print(Leaderboard.display(tournament))
```

Leaderboard is sorted by **descending score**, then by number of wins.

| Result | Points |
|---|---|
| Win | 1 pt |
| Draw | 0.5 pt |
| Loss | 0 pt |

Columns displayed: Rank · Player · Played · Wins · Draws · Losses · Score

---

## Class Overview

```
Player
├── username, email, date_of_birth, gender, registration_date, elo
├── age (computed property)
└── display()

Tournament
├── name, location, number_of_players, elo, categories, type
├── registration_deadline, status, current_round_number
├── tournament_list, match_list
├── add_player(player) / remove_tournament()
├── start_tournament()
├── next_round()
├── display_tournament() / display_round()
└── check_registration(player)

Match
├── id, tournament_id, white_player, black_player, round_number, result
├── is_played (property)
├── set_result(Match_result) / reset_result()
├── get_points_for(player)
├── display()
└── generate_round_robin_double(tournament)  [static]

Leaderboard
├── get_standings(tournament)  [static]
└── display(tournament)        [static]
```

---

## Enumerations

```python
class Gender(Enum):
    MALE   = "Male"
    FEMALE = "Female"
    MIXTE  = "Mixte"

class Categories(Enum):
    JUNIOR  = "Junior"
    SENIOR  = "Senior"
    VETERAN = "Veteran"

class Type(Enum):
    MALE   = "Male Only"
    FEMALE = "Women Only"
    MIXTE  = "Mixte"

class Status(Enum):
    WAITING   = "Waiting for players..."
    PROGRESS  = "In progress"
    COMPLETED = "Completed !"

class Match_result(Enum):
    NOT_PLAYED   = "Not played"
    WHITE_PLAYER = "White player"
    BLACK_PLAYER = "Black player"
    DRAW         = "Draw"
```

---

## Example Output

```
╔══════════════════════════════════════════════════╗
║           ♟  TOURNAMENT : Mondial                ║
╠══════════════════════════════════════════════════╣
║  📍 Location      : Spain                        ║
║  👥 Max players   : 4                            ║
║  ⚡ Min ELO       : 1800                         ║
║  🏷  Category     : Senior                       ║
║  🚻 Type          : Mixte                        ║
║  📌 Status        : In progress                  ║
║  📅 Deadline      : 17/02/2026                   ║
║  🔁 Current round : 1                            ║
╚══════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════╗
║                 🏆  LEADERBOARD : Mondial               ║
║                        Round 2                           ║
╠══════════════════════════════════════════════════════════╣
║  #    Player         Played  Wins  Draws  Losses  Score  ║
╠──────────────────────────────────────────────────────────╣
║  🥇   Alice              1     1      0       0     1.0  ║
║  🥈   Bob               1     0      0       1     0.0  ║
╚══════════════════════════════════════════════════════════╝
```

---

## Author

Project developed as part of a chess tournament management exercise in Python (OOP).