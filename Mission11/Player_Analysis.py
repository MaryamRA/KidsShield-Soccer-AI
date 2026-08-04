import streamlit as st
from Artin_FC_data import df
import pandas as pd

player_name = st.selectbox("Choose Player:", df["name"])
player_data = df[df["name"] == player_name].iloc[0]


col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Speed")
    st.write(player_data["speed"])
with col2:
    st.subheader("Stamina")
    st.write(player_data["stamina"])
with col3:
    st.subheader(f"Shooting")
    st.write(player_data["shooting"])


    st.divider()




st.subheader(f"Attributes for {player_name}")

attributes = pd.DataFrame({
    "Attribute": [
        "Speed",
        "Stamina",
        "Shooting",
        "Passing",
        "Defending",
        "Overall Goals",
        "Overall Assists"
    ],

    "Rating": [
        player_data["speed"],
        player_data["stamina"],
        player_data["shooting"],
        player_data["passing"],
        player_data["defending"],
        player_data["total_goals"],
        player_data["total_assists"]
    ]
}).set_index("Attribute")

st.bar_chart(attributes)

