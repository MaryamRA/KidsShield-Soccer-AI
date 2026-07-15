# =====================================================================
# 🧱                  THE SOCCER ANALYTICS LIBRARY --- VERSION 1.0
# =====================================================================

def calculate_goals(player_profile):
    total_goals = 0

    # Loop through the historical goals list
    for g in player_profile["goals"]:
        total_goals = total_goals + g
    return total_goals


def calculate_assists(sd):
    total_assists = 0

    for a in sd["assists"]:
        total_assists = total_assists + a
    return total_assists


def calculate_historical_contributions(player_profile):
    total_goals = calculate_goals(player_profile)
    total_assists =calculate_assists(player_profile)
    return total_goals + total_assists


def overall_rating(player):
    return (player_stats["speed"] + player_stats['passing'] + player_stats['shooting'] + player_stats['defending']) / 4


def match_result(home_score, away_score):

    if home_score > away_score:
        print("Win")

    elif home_score < away_score:
        print("Loss")

    else:
        print("Draw")


def goal_difference(home_score, away_score):
    return abs(home_score - away_score)


def player_summary(player):
    print("====================")
    print("   PLAYER REPORT    ")
    print(f"Name: {player['name']}")
    print(f"Position: {player['position']}")
    print(f"Goals: {player['goals']}")
    print(f"Assists: {player['assists']}")
    print("====================")

