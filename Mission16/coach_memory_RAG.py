# ============================================================
# ⚽ MISSION 16 — ANSWER KEY
# Artin FC AI Soccer Agent
# Persistent Memory + Team Knowledge + RAG
# ============================================================

import os
import json
import pandas as pd
import streamlit as st

from google import genai

import memory_toolbox as mt
import knowledge_toolbox as kt

from Artin_FC_data import Artin_FC_v3


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
    "Mission 16 — Persistent Memory + Team Knowledge + RAG"
)


st.write(
    """
Your AI Soccer Agent can now use three sources
of information:

🧠 Player Memory

⚽ Team Knowledge

📚 Soccer Knowledge
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


memory = mt.recall()


if memory:

    st.json(memory)

else:

    st.info(
        "The agent does not have any memories yet."
    )


# ============================================================
# SECTION 3 — TEAM KNOWLEDGE
# ============================================================

st.header("⚽ Artin FC Team Knowledge")


# Artin_FC_v3 is a list of dictionaries.
# Convert it into a DataFrame.

team_data = pd.DataFrame(
    Artin_FC_v3
)


# Display team data

st.dataframe(
    team_data,
    use_container_width=True
)


# ============================================================
# SECTION 4 — SELECT A PLAYER
# ============================================================

st.header("👤 Select a Player")


selected_player = st.selectbox(
    "Choose a player:",
    team_data["name"].tolist()
)


# Find the selected player's row

player_data = team_data[
    team_data["name"] == selected_player
]


st.write(
    f"### {selected_player}'s Team Data"
)


st.dataframe(
    player_data,
    use_container_width=True
)


# ============================================================
# SECTION 5 — LOAD SOCCER KNOWLEDGE
# ============================================================

st.header("📚 Soccer Knowledge")


try:

    knowledge = kt.load_knowledge(
        "soccer_knowledge.txt"
    )

    st.success(
        "Soccer knowledge loaded successfully."
    )

except FileNotFoundError:

    knowledge = []

    st.error(
        "soccer_knowledge.txt was not found."
    )


# ============================================================
# SECTION 6 — SEARCH SOCCER KNOWLEDGE
# ============================================================

st.subheader(
    "🔎 Search Soccer Knowledge"
)


keyword = st.text_input(
    "Enter a soccer topic:",
    value="winger"
)


if st.button(
    "📚 Search Knowledge"
):

    if knowledge:

        retrieved_results = kt.search_knowledge(
            knowledge,
            keyword
        )


        if retrieved_results:

            retrieved_info = "\n\n".join(
                retrieved_results
            )


            st.subheader(
                "📖 Retrieved Soccer Knowledge"
            )


            st.write(
                retrieved_info
            )


        else:

            st.warning(
                "No matching soccer knowledge was found."
            )

    else:

        st.warning(
            "The knowledge base is empty."
        )


# ============================================================
# SECTION 7 — ASK GEMINI
# ============================================================

st.header("🤖 Ask My AI Coach")


user_question = st.text_input(
    "Ask your coach:",
    value="What should I improve?"
)


if st.button(
    "⚽ Ask Coach",
    type="primary"
):

    if not user_question:

        st.warning(
            "Please enter a question."
        )

        st.stop()


    if "GEMINI_API_KEY" not in os.environ:

        st.error(
            "GEMINI_API_KEY was not found."
        )

        st.stop()


    # ========================================================
    # RECALL PLAYER MEMORY
    # ========================================================

    memory = mt.recall()

 # ========================================================
    # RETRIEVE SOCCER KNOWLEDGE
    # ========================================================

    if knowledge:

        retrieved_results = kt.search_knowledge(
            knowledge,
            keyword
        )


        if retrieved_results:

            retrieved_info = "\n\n".join(
                retrieved_results
            )

        else:

            retrieved_info = (
                "No matching soccer knowledge was found."
            )

    else:

        retrieved_info = (
            "No soccer knowledge is available."
        )



   
    # ========================================================
    # BUILD THREE-SOURCE PROMPT
    # ======================================================
    prompt = f"""
You are an AI Soccer Coach for Artin FC.

You have three sources of information.

============================================================
SOURCE 1 — PLAYER MEMORY
============================================================

{memory}


============================================================
SOURCE 2 — TEAM KNOWLEDGE
============================================================

{player_data.to_string(index=False)}


============================================================
SOURCE 3 — SOCCER KNOWLEDGE
============================================================

{retrieved_info}


============================================================
PLAYER QUESTION
============================================================

{user_question}


============================================================
INSTRUCTIONS
============================================================

Use the three sources to provide
personalized soccer coaching advice.

Use the player's memory when relevant.

Use the player's team statistics when relevant.

Use the retrieved soccer knowledge when relevant.

Do not invent statistics.

Do not invent facts about the player.

If information is not available,
say that it is not available.

Give simple, practical advice that
a young soccer player can understand.
"""


    # ========================================================
    # ASK GEMINI
    # ========================================================

    client = genai.Client()


    with st.spinner(
        "Your AI Coach is thinking..."
    ):

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )


    # ========================================================
    # DISPLAY ANSWER
    # ========================================================

    st.subheader(
        "🤖 AI Coach Advice"
    )


    st.write(
        response.text
    )


# ============================================================
# SECTION 8 — FORGET MEMORY
# ============================================================

st.header("🗑️ Forget Something")


st.write(
    "Remove a piece of information from the agent's memory."
)


memory = mt.recall()


if memory:

    memory_key_to_forget = st.selectbox(
        "Choose something to forget:",
        list(memory.keys())
    )


    if st.button(
        "🗑️ Forget"
    ):

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


# ============================================================
# SECTION 9 — SHOW THE THREE SOURCES
# ============================================================

st.divider()

st.header(
    "🧠⚽📚 My AI Coach's Three Sources"
)


col1, col2, col3 = st.columns(3)


with col1:

    st.subheader(
        "🧠 Memory"
    )

    st.write(
        "What the agent remembers about the player."
    )


with col2:

    st.subheader(
        "⚽ Team Data"
    )

    st.write(
        "Player statistics from Artin_FC_v3."
    )


with col3:

    st.subheader(
        "📚 Soccer Knowledge"
    )

    st.write(
        "Soccer information retrieved from documents."
    )


# ============================================================
# SECTION 10 — FINAL MISSION MESSAGE
# ============================================================

st.divider()


st.success(
    """
🎉 Mission 16 Complete!

Your AI Soccer Agent can now:

🧠 Remember information permanently

⚽ Read team and player data

📚 Retrieve soccer knowledge

🤖 Combine all three sources

🏆 Provide personalized coaching advice
"""
)