# ============================================================
# ⚽ MISSION 15
# Artin FC AI Soccer Agent
# Persistent Memory + Gemini
# ============================================================

import os
import json
import pandas as pd
import streamlit as st

from google import genai

import memory_toolbox as mt


# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="Artin FC AI Soccer Agent",
    page_icon="⚽",
    layout="centered"
)


st.title("⚽ Artin FC AI Soccer Agent")

st.caption(
    "Mission 15 — Persistent Memory"
)


st.write(
    """
Your AI Soccer Agent can now remember information,
save it permanently, recall it later, and forget
information when necessary.
"""
)


# ============================================================
# LOAD MEMORY SAFELY
# ============================================================

def load_memory():

    if os.path.exists(mt.MEMORY_FILE_NAME):

        return mt.recall()

    else:

        return {}


# ============================================================
# LOAD PLAYER MEMORY
# ============================================================

memory = load_memory()


# ============================================================
# SECTION 1 — TEACH THE AGENT
# ============================================================

st.header("🧠 Teach My Agent")

st.write(
    "Add new information to your AI Soccer Agent's memory."
)


memory_key = st.text_input(
    "Memory Key",
    placeholder="Example: position"
)


memory_value = st.text_input(
    "Memory Value",
    placeholder="Example: Right Winger"
)


if st.button("💾 Remember"):

    if memory_key and memory_value:

        memory = mt.memorize(
            memory,
            memory_key,
            memory_value
        )

        mt.remember(
            memory,
            mt.MEMORY_FILE_NAME
        )

        st.success(
            "New information saved to memory!"
        )

    else:

        st.warning(
            "Please enter both a key and a value."
        )


# ============================================================
# SECTION 2 — SHOW MEMORY
# ============================================================

st.header("📖 My Soccer Memory")


memory = load_memory()


if memory:

    st.json(memory)

else:

    st.info(
        "The agent does not have any memories yet."
    )


# ============================================================
# SECTION 3 — ASK GEMINI
# ============================================================

st.header("🤖 Ask My AI Coach")


user_question = st.text_input(
    "Ask your coach:",
    value="What should I improve?"
)


if st.button("⚽ Ask Coach"):

    if not user_question:

        st.warning(
            "Please enter a question."
        )

    elif "GEMINI_API_KEY" not in os.environ:

        st.error(
            "GEMINI_API_KEY was not found."
        )

    else:

        # ----------------------------------------------------
        # Recall memory
        # ----------------------------------------------------

        memory = load_memory()


        # ----------------------------------------------------
        # Build prompt
        # ----------------------------------------------------

        prompt = f"""
You are an AI Soccer Coach.

The player has the following information
stored in persistent memory:

{memory}

The player asks:

{user_question}

Use the player's memory to answer the question.

Only use information available in the memory.
Do not invent player statistics or facts.

Give simple and useful soccer coaching advice.
"""


        # ----------------------------------------------------
        # Ask Gemini
        # ----------------------------------------------------

        client = genai.Client()


        with st.spinner(
            "Your AI Coach is thinking..."
        ):

            response = client.models.generate_content(

                model="gemini-2.5-flash",

                contents=prompt
            )


        # ----------------------------------------------------
        # Display answer
        # ----------------------------------------------------

        st.subheader(
            "🤖 AI Coach Advice"
        )

        st.write(
            response.text
        )


# ============================================================
# SECTION 4 — FORGET MEMORY
# ============================================================

st.header("🗑️ Forget Something")


st.write(
    "Remove a piece of information from the agent's memory."
)


memory = load_memory()


if memory:

    memory_key_to_forget = st.selectbox(
        "Choose something to forget:",
        list(memory.keys())
    )


    if st.button("🗑️ Forget"):

        memory = mt.forget(
            memory,
            memory_key_to_forget
        )


        mt.remember(
            memory,
            mt.MEMORY_FILE_NAME
        )


        st.success(
            f"'{memory_key_to_forget}' "
            "has been removed from memory."
        )


        st.rerun()

else:

    st.info(
        "There is nothing to forget."
    )


