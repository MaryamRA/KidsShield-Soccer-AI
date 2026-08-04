import streamlit as st
from Artin_FC_data import df
import pandas as pd
import google.generativeai as genai


st.set_page_config(
    page_title="Coach Command Center",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Coach Command Center")
st.write("Analyze players by position and receive AI coaching advice.")

player_name = st.sidebar.selectbox("Choose Player:", df["name"])
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

st.title("📈 Team Statistics")

st.header("🔍 Dynamic Squad Filter")

selected_position = st.selectbox("Filter Squad by Position:", ["All", "Forward", "Midfielder", "Defender", "GK"])

if selected_position == "All":
    filtered_df = df
else:
    filtered_df = df[df["position"] == selected_position]

st.dataframe(filtered_df[["name", "position", "stamina", "speed", "shooting", "total_goals"]], use_container_width=True)


st.divider()


st.metric("Average Team Speed", f"{df['speed'].mean():.1f}")
st.subheader("Speed Comparison")
st.bar_chart(df[["name", "speed"]].set_index("name"))


# Team-Level Comparison Chart (Many Players)
st.header("📈 Interactive Player Comparison Chart")

# Make player names the row labels. you explicitly tell Streamlit: Use the player names as the labels for the chart.
df = df.set_index("name")

# Select only the columns you want
chart_data = df[["stamina", "speed", "passing", "shooting", "defending", "total_goals", "total_assists"]]

# Display the chart
st.bar_chart(chart_data)

st.divider()

st.title("Coaching Rules")

#player_name2 = st.selectbox("Choose Player:", df["name"])
#player_data2 = df[df["name"] == player_name2].iloc[0]

selected_stamina= st.slider("Stamina slider", min_value = 0, max_value= 100, value=int(player_data["stamina"]))
selected_speed= st.slider("Speed slider", min_value = 0, max_value= 100, value=int(player_data["speed"]))

if (selected_stamina >= 85) & (selected_speed >= 90):
    st.success("Excellent Atheticism!")
elif (selected_stamina >= 85) & (selected_speed < 90):
    st.warning("Excellent stamina, but speed needs improvment.")
elif (selected_stamina < 85) & (selected_speed > 90):
    st.warning("Excellent speed, but stamina needs improvment.")
else:
    st.error("Stamina and speed both need improvment.")
st.divider()


st.sidebar.title("⚽ Coach Menu")

st.title("🤖 AI Assistant Coach")

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

question = st.text_input("Ask AI Coach:")


mode= st.sidebar.radio(
    "Choose coaching style:",
    [
        "Attack Focus Coach",
        "Defense Focus Coach",
        "Fitness Focus Coach"
    ]
)
        
if st.button("Get Tactical Advice"):
    if question:

        prompt = f"""
You are a {mode}

Below is information about the Artin FC squad.

{df[['position', 'speed', 'stamina', 'total_goals']].to_string(index=False)}

User's Question:
{question}

Using the squad information above, provide clear, practical, and personalized coaching advice.

If the coach selects:

Attack Focus

Gemini should answer:

Focus on shooting, positioning, and creating chances.

If:

Defense Focus

Gemini should analyze:

Defensive positioning and recovery runs.`
"""

        response = model.generate_content(prompt)

        st.markdown("### 🤖 AI Tactical Advice")
        st.write(response.text)