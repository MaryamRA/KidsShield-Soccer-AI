import streamlit as st
import pandas as pd
from Artin_FC_data import df

st.set_page_config(page_title="Team Statistics", page_icon="📈", layout="wide")
st.sidebar.title("⚽ Coach Menu")

st.title("📈 Team Statistics")
st.metric("Average Team Speed", f"{df['speed'].mean():.1f}")
st.subheader("Speed Comparison")
st.bar_chart(df[["name", "speed"]].set_index("name"))


# Team-Level Comparison Chart (Many Players)
st.header("📈 Interactive Player Comparison Chart")

# Make player names the row labels. you explicitly tell Streamlit: Use the player names as the labels for the chart.
dfs = df.set_index("name")

# Select only the columns you want
chart_data = dfs[["stamina", "speed", "passing", "shooting", "defending", "total_goals", "total_assists"]]

# Display the chart
st.bar_chart(chart_data)


st.dataframe(df)