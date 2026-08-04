import streamlit as st
import google.generativeai as genai
from Artin_FC_data import df
import pandas as pd

st.set_page_config(page_title="AI Assistant Coach", page_icon="🤖", layout="wide")
st.sidebar.title("⚽ Coach Menu")

st.title("🤖 AI Assistant Coach")

genai.configure(
    api_key=st.secrets["GEMINI_API_KEY"]
)

model = genai.GenerativeModel("gemini-3.5-flash")


st.title("⚽ Personalized AI Soccer Coach")


player = st.selectbox(
    "Choose your player:", df["name"])


style = st.radio(
    "Choose coaching style:",
    [
        "Motivational Coach",
        "Technical Coach",
        "Strict Performance Coach"
    ]
)


if st.button("Get Advice"):

    prompt = f"""

    You are a {style}.

    You are coaching {player}.

    Provide practical soccer advice.

    """


    response = model.generate_content(prompt)


    st.success("AI Coach Response")

    st.write(response.text)