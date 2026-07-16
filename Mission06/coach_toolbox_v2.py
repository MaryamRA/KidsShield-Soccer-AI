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

def needs_passing_practice(player):
    # Calculate accuracy across their pass tracking lists via loop
    total_comp = 0
    total_att = 0
    for cp in player["passes_completed"]:
        total_comp = total_comp + cp
    for tp in player["total_passes"]:
        total_att = total_att + tp

    accuracy = (total_comp / total_att) * 100
    return accuracy < 80.0


def passing_accuracy(player):
    total_comp = 0
    total_att = 0
    for cp in player["passes_completed"]:
        total_comp = total_comp + cp
    for tp in player["total_passes"]:
        total_att = total_att + tp
    accuracy = (total_comp / total_att) * 100
    return accuracy

def needs_rest(player):

    if calculate_goals(player) > 5:
        return True

    else:
        return False


def is_forward(player):
    if player["position"] in ["LW", "CF", "RW"]:
        return True

    else:
        return False



def needs_endurance_training(player):
    if is_forward(player) == True and passing_accuracy(player) < 85:
        return True

    else:
        return False


def excellent_stamina(player):
    for cp in player["passes_completed"]:
        if cp <= 20:
            return False
    return True


def calculate_overall_rating(player):
    # your code here
    if player["position"] == "GK":
        rating  = (player["stamina"] * 0.40) + (player["speed"] * 0.20)
    else:
        rating = (player["defending"] + player["stamina"] + player["speed"] + player["shooting"]) / 4 
        
    return rating


def coach_decision(player):

    # your code here
    if needs_rest(player) == True:
        return "Recovery Day"
    
    if needs_endurance_training(player) == True:
        return "Endurance Training."
    
    if needs_passing_practice(player) == True:
        return "Passing Practice."

    else:
        return "Ready for Match."


def generate_ai_tactical_recommendation(player):
    # your code here
    if player["defending"] > 80:
        return "Solid defensive anchor. Hold the backline."

    if player["speed"] > 90 and player["shooting"] > 80:
        return "Winger breakout threat. Focus on flank overlaps."

    elif player["shooting"] > 90:
        return "Target striker. Look for direct shots inside the box."
    
    else:
        return "Tactical supporting playmaker. Distribute cleanly."
