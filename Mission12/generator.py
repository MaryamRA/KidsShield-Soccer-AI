import json

cells = []

def add_markdown(source_text):
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in source_text.strip().split("\n")]
    })

def add_code(source_text):
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in source_text.strip().split("\n")]
    })

# Title & Learning Goals
add_markdown("""# Mission 13: Player Tracking & AI Performance Analysis 🏃🤖

## 🎯 New Learning Goal
At the end of this mission, your AI Soccer Coach can answer:
> *"What happened to Artin during the match?"*

### The system will extract:
#### 📊 Movement Data
* ✅ Player location
* ✅ Distance covered
* ✅ Speed
* ✅ Acceleration
* ✅ Direction changes
* ✅ Time spent in different zones

#### ⚽ Soccer Intelligence
* ✅ Ball possession estimation
* ✅ Attacking movement
* ✅ Defensive recovery
* ✅ Tactical recommendations from Gemini""")

# Phase 1
add_markdown("""---
# Phase 1 — Player Tracking

### Input & Output Pipeline:
* **Input:** Soccer Video
* **AI:** `YOLO Detection` + `Object Tracking`
* **Output Table Format:** `Frame | Time | Player ID | X | Y`

| Frame | Time | Player ID | X | Y |
|---|---|---|---|---|
| 1 | 0.0s | 4 | 53 | 28 |
| 2 | 0.04s | 4 | 54 | 29 |
| 3 | 0.08s | 4 | 56 | 31 |""")

add_code("""import pandas as pd
import numpy as np

# Simulated Phase 1 Tracking Data
tracking_data = [
    {"frame": 1, "time": 0.00, "player_id": 4, "x": 53.0, "y": 28.0},
    {"frame": 2, "time": 0.04, "player_id": 4, "x": 54.0, "y": 29.0},
    {"frame": 3, "time": 0.08, "player_id": 4, "x": 56.0, "y": 31.0},
    {"frame": 4, "time": 0.12, "player_id": 4, "x": 59.0, "y": 33.0},
    {"frame": 5, "time": 0.16, "player_id": 4, "x": 63.0, "y": 36.0},
    {"frame": 6, "time": 0.20, "player_id": 4, "x": 68.0, "y": 40.0},
]

df_tracking = pd.DataFrame(tracking_data)
print("Phase 1 Raw Tracking Output:")
print(df_tracking)""")

# Phase 2
add_markdown("""---
# Phase 2 — Extract Movement Features

In this phase, we calculate movement metrics from frame-by-frame coordinate tracking data.

### 1. Distance Covered ⚽
The AI calculates movement between consecutive coordinates:

$$\\text{Distance} = \\sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$$

* **Example:** Frame 1: $(53, 28) \\rightarrow$ Frame 2: $(56, 31) \\implies \\text{Distance} = 4.2 \\text{ yards}$
* **Total Distance:** Sum of all frame-to-frame movements.

### 2. Speed 🏃
$$\\text{Speed} = \\frac{\\text{Distance}}{\\text{Time}}$$

* **Example:** $\\text{Distance} = 4\\text{ meters}, \\text{Time} = 0.5\\text{ seconds} \\implies \\text{Speed} = 8\\text{ m/s}$
* Reports **Average Speed** and **Maximum Speed**.

### 3. Acceleration 🚀
Detects transitions such as **Sprinting**, **Stopping**, and **Changing Direction**:
* **Walking:** $\\approx 2\\text{ m/s}$
* **Sprint:** $\\approx 7\\text{ m/s}$

$$\\text{Acceleration} = \\frac{\\text{Speed}_2 - \\text{Speed}_1}{\\Delta t}$$

### 4. Movement Zones 🗺️
Divide the pitch into quadrants:

| Defense | Midfield |
|---|---|
| Attack | Final Third |

Calculate percentage of total time spent in each zone (e.g., Artin: Defense 15%, Midfield 55%, Final Third 30%).""")

add_code("""def extract_movement_features(df):
    df = df.copy()

    # 1. Distance covered per step
    df["dx"] = df["x"].diff().fillna(0)
    df["dy"] = df["y"].diff().fillna(0)
    df["distance"] = np.sqrt(df["dx"]**2 + df["dy"]**2)

    # 2. Speed (Distance / dt)
    df["dt"] = df["time"].diff().fillna(0.04) # 25 fps timestep
    df["speed"] = df["distance"] / df["dt"]

    # 3. Acceleration
    df["acceleration"] = df["speed"].diff().fillna(0) / df["dt"]

    # 4. Movement Zones
    def get_zone(row):
        if row["x"] < 40:
            return "Defense"
        elif row["x"] < 80:
            return "Midfield"
        else:
            return "Final Third"

    df["zone"] = df.apply(get_zone, axis=1)
    return df

df_features = extract_movement_features(df_tracking)
print("Extracted Movement Features:")
print(df_features[["frame", "time", "distance", "speed", "acceleration", "zone"]])""")

# Phase 3
add_markdown("""---
# Phase 3 — Ball Possession Detection ⚽

The AI calculates the proximity between player position and ball position for every frame:

$$\\text{Distance}(\\text{Player}, \\text{Ball}) = \\sqrt{(x_{\\text{player}} - x_{\\text{ball}})^2 + (y_{\\text{player}} - y_{\\text{ball}})^2}$$

### Possession Rule:
$$\\text{If Distance} < \\text{Threshold (e.g., 2.0 meters)} \\implies \\text{Possession = True}$$

| Frame | Player | Ball Distance | Possession |
|---|---|---|---|
| 1 | 4 | 1.2 m | Yes |
| 2 | 4 | 0.8 m | Yes |
| 3 | 4 | 8.0 m | No |""")

add_code("""possession_data = [
    {"frame": 1, "player_x": 53.0, "player_y": 28.0, "ball_x": 53.8, "ball_y": 28.5},
    {"frame": 2, "player_x": 54.0, "player_y": 29.0, "ball_x": 54.5, "ball_y": 29.3},
    {"frame": 3, "player_x": 56.0, "player_y": 31.0, "ball_x": 64.0, "ball_y": 38.0},
]

df_possession = pd.DataFrame(possession_data)
threshold = 2.0

df_possession["ball_distance"] = np.sqrt(
    (df_possession["player_x"] - df_possession["ball_x"])**2 +
    (df_possession["player_y"] - df_possession["ball_y"])**2
)

df_possession["has_possession"] = df_possession["ball_distance"] < threshold

print("Possession Tracking Results:")
print(df_possession[["frame", "ball_distance", "has_possession"]])""")

# Phase 4
add_markdown("""---
# Phase 4 — Create Player Report

Aggregated performance metrics summary for **Artin**:

* **Player:** Artin
* **Position:** Right Winger
* **Distance Covered:** 6.4 km
* **Average Speed:** 5.1 km/h
* **High Intensity Runs:** 12
* **Ball Possession:** 38 seconds
* **Most Occupied Zone:** Right Wing
* **Attacking Runs:** 8
* **Defensive Recoveries:** 5""")

add_code("""artin_report = {
    "player_name": "Artin",
    "position": "Right Winger",
    "distance_km": 6.4,
    "average_speed_kmh": 5.1,
    "max_speed_kmh": 28.4,
    "high_intensity_runs": 12,
    "possession_time_sec": 38,
    "most_occupied_zone": "Right Wing",
    "final_third_time_pct": 30,
    "attacking_runs": 8,
    "defensive_recoveries": 5
}

print("Artin Performance Summary Dictionary:")
for k, v in artin_report.items():
    print(f" • {k.replace('_', ' ').title()}: {v}")""")

# Phase 5
add_markdown("""---
# Phase 5 — Gemini AI Coach 🤖

Connecting Gemini LLM to process extracted player statistics and deliver tactical coaching advice.""")

add_code("""import google.generativeai as genai

player_statistics = {
    "position": "Right winger",
    "distance": 6.4,
    "average_speed": 5.1,
    "final_third_time": 30,
    "possession_time": 38,
    "defensive_runs": 5,
    "attacking_runs": 8
}

prompt = f\"\"\"You are a UEFA professional soccer coach.

Analyze this player's performance:
{player_statistics}

Provide:
1. Strengths
2. Weaknesses
3. Tactical improvements
4. Training recommendations\"\"\"

print("Prompt sent to Gemini:")
print(prompt)""")

# Final Boss
add_markdown("""---
# Final Boss Challenge 🏆: Artin FC AI Tactical Analyst

Constructing the Streamlit dashboard app script `app_mission13.py` directly from the notebook.
