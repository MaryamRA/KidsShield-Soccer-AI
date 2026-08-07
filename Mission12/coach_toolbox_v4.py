# =====================================================================
# 🧱                  THE SOCCER ANALYTICS LIBRARY --- VERSION 1.0
# =====================================================================

import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch

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


def elite_status(player):
    player_rating = ct.calculate_overall_rating(player)
    if player_rating > 85:
        print("ELITE status")
    else:
        print("NOT elite status")



def pitch_plot(player, position, csv_file):

    movement_df = pd.read_csv(csv_file)

   x_coordinates = movement_df["x_coordinates"]
   y_coordinates = movement_df["y_coordinates"]


    pitch = Pitch(
        pitch_type='statsbomb',
        pitch_color='#aabb97',
        line_color='white'
    )

    fig, ax = pitch.draw(figsize=(10,7))


    bin_statistic = pitch.bin_statistic(
        x_coordinates,
        y_coordinates,
        statistic='count',
        bins=(12,8)
    )


    pitch.heatmap(
        bin_statistic,
        ax=ax,
        cmap='Reds',
        edgecolor='white',
        alpha=0.6
    )


    pitch.scatter(
        x_coordinates,
        y_coordinates,
        c='black',
        s=50,
        ax=ax
    )


    plt.title(
        f"{player}'s Soccer Heatmap - {position}"
    )


    return fig


def create_player_csv(position, filename):

    if position == "Left Winger":
        data = {
            'frame': list(range(1, 21)),
            'x_coordinates' : [10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105],
            'y_coordinates' : [10,12,15,18,20,18,15,12,10,15,18,20,22,25,28,30,35,38,40,42]
        }

    elif position == "Striker":
         data = {
            'frame': list(range(1, 21)),
            'x_coordinates' : [70,75,80,85,90,95,100,102,105,108,110,112,115,108,104,100,95,90,88,110],
            'y_coordinates' : [35,38,40,42,40,38,35,37,40,42,39,36,40,45,48,50,45,42,38,35]
        }     
    elif position == "Midfielder" :
         data = {
            'frame': list(range(1, 21)),
            'x_coordinates' : [35,40,45,50,55,60,65,70,60,55,50,45,40,55,65,75,70,60,50,45],
            'y_coordinates' : [25,30,35,40,45,40,35,30,25,20,25,30,35,45,50,45,40,35,30,25]
        }     
    elif position == "Right Defender":
         data = {
            'frame': list(range(1, 21)),
            'x_coordinates' : [15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110],
            'y_coordinates' : [70,72,68,70,72,74,76,74,72,70,68,70,72,74,76,72,68,65,60,55]
         }  
    else:
        print("❌ Invalid position.")
        return

    # Create DataFrame
    df = pd.DataFrame(data)

    # Save CSV
    df.to_csv(filename, index=False)

    print(f"✅ {filename} created successfully.")  