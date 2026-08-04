import os
print(os.listdir())
import streamlit as st
from Artin_FC_data import df

st.set_page_config(page_title="Artin FC Dashboard", page_icon="⚽", layout="wide")

st.sidebar.title("⚽ Coach Menu")
st.sidebar.info("Use the sidebar to navigate between pages.")

st.title("⚽ Artin FC Coaching Dashboard")
st.subheader("Welcome Coach Artin!")

st.markdown("""
Welcome to your professional soccer analytics suite.

### 📌 Features:
* **🏃 Player Analysis:** View metrics, performance attributes, and radar/bar charts.
* **📈 Team Statistics:** Explore roster-wide averages and player comparisons.
* **🤖 AI Coach:** Consult Gemini for tactical insights and roster recommendations.
""")

st.write(f"Number of Players: {len(df)}")
st.write(f"Average Team Speed: {df["speed"].mean()}")
st.write(f"Average Team Stamina: {df["stamina"].mean()}")