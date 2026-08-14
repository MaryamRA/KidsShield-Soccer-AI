import pandas as pd

Artin_FC_v3 =

[
{'name': 'Artin', 'age': 15, 'position': 'Forward', 'goals': [2, 1, 0, 3], 'assists': [1, 0, 2, 1], 'passes_completed': [25, 30, 22, 28], 'total_passes': [28, 32, 26, 30], 'passing': 84, 'defending': 45, 'stamina': 90, 'speed': 92, 'shooting': 88, 'total_goals': 6, 'total_assists': 4},

{'name': 'Messi', 'age': 34, 'position': 'Forward', 'goals': [2, 3, 1, 2], 'assists': [1, 1, 2, 0], 'passes_completed': [40, 42, 38, 45], 'total_passes': [42, 43, 40, 46], 'passing': 85, 'defending': 38, 'stamina': 85, 'speed': 89, 'shooting': 96, 'total_goals': 8, 'total_assists': 4},

{'name': 'Jahanbakhsh', 'age': 32, 'position': 'Forward', 'goals': [0, 1, 0, 1], 'assists': [1, 0, 1, 0], 'passes_completed': [20, 18, 22, 19], 'total_passes': [25, 24, 26, 23], 'passing': 68, 'defending': 50, 'stamina': 80, 'speed': 85, 'shooting': 80, 'total_goals': 2, 'total_assists': 2},

{'name': 'Maradona', 'age': 39, 'position': 'Midfielder', 'goals': [1, 2, 1, 1], 'assists': [2, 1, 3, 1], 'passes_completed': [35, 38, 32, 36], 'total_passes': [38, 40, 35, 39], 'passing': 93, 'defending': 40, 'stamina': 82, 'speed': 88, 'shooting': 92, 'total_goals': 5, 'total_assists': 7},

{'name': 'Zidane', 'age': 38, 'position': 'Midfielder', 'goals': [0, 1, 0, 0], 'assists': [1, 2, 1, 2], 'passes_completed': [38, 42, 40, 41], 'total_passes': [40, 45, 42, 44], 'passing': 83, 'defending': 65, 'stamina': 84, 'speed': 80, 'shooting': 84, 'total_goals': 1, 'total_assists': 6},

{'name': 'Iniesta', 'age': 25, 'position': 'Midfielder', 'goals': [0, 0, 1, 0], 'assists': [2, 1, 1, 1], 'passes_completed': [45, 48, 42, 46], 'total_passes': [47, 50, 45, 48], 'passing': 77, 'defending': 75, 'stamina': 84, 'speed': 70, 'shooting': 74, 'total_goals': 1, 'total_assists': 5},

{'name': 'Marcelo', 'age': 30, 'position': 'Defender', 'goals': [0, 1, 0, 0], 'assists': [1, 1, 2, 0], 'passes_completed': [30, 32, 28, 34], 'total_passes': [34, 36, 32, 38], 'passing': 73, 'defending': 75, 'stamina': 84, 'speed': 80, 'shooting': 84, 'total_goals': 1, 'total_assists': 4},

{'name': 'Pique', 'age': 33, 'position': 'Defender', 'goals': [0, 0, 1, 0], 'assists': [0, 0, 0, 1], 'passes_completed': [22, 24, 20, 25], 'total_passes': [25, 26, 22, 28], 'passing': 93, 'defending': 88, 'stamina': 80, 'speed': 72, 'shooting': 65, 'total_goals': 1, 'total_assists': 1},

{'name': 'Maldini', 'age': 27, 'position': 'Defender', 'goals': [0, 0, 0, 0], 'assists': [0, 0, 1, 0], 'passes_completed': [18, 22, 21, 19], 'total_passes': [20, 24, 22, 21], 'passing': 83, 'defending': 94, 'stamina': 85, 'speed': 82, 'shooting': 60, 'total_goals': 0, 'total_assists': 1},

{'name': 'Dani Alves', 'age': 38, 'position': 'Defender', 'goals': [0, 0, 0, 1], 'assists': [2, 1, 1, 2], 'passes_completed': [32, 35, 30, 33], 'total_passes': [36, 38, 34, 37], 'passing': 73, 'defending': 80, 'stamina': 89, 'speed': 88, 'shooting': 72, 'total_goals': 1, 'total_assists': 6},

{'name': 'Beiranvand', 'age': 30, 'position': 'GK', 'goals': [0, 0, 0, 0], 'assists': [0, 0, 0, 0], 'passes_completed': [15, 12, 18, 14], 'total_passes': [22, 20, 25, 21], 'passing': 63, 'defending': 15, 'stamina': 75, 'speed': 65, 'shooting': 10, 'total_goals': 0, 'total_assists': 0}
]


df = pd.DataFrame(Artin_FC_v3)
print (df.head())
