{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# ⚽ Mission 14: Meet Your AI Soccer Coach Agent\n",
    "\n",
    "## From AI Model to AI Agent\n",
    "\n",
    "In Mission 13, we taught AI how to see Artin.\n",
    "\n",
    "The computer could:\n",
    "- detect players\n",
    "- track Artin\n",
    "- measure movement\n",
    "- calculate distance\n",
    "- estimate speed\n",
    "- identify tactical zones\n",
    "\n",
    "But there is an important question:\n",
    "> Can AI use this information to act like a soccer coach?\n",
    "\n",
    "That is where AI agents come in.\n",
    "\n",
    "In this mission, we will build the first version of:\n",
    "# ⚽ Artin FC AI Soccer Coach\n",
    "\n",
    "The coach will eventually be able to:\n",
    "- remember Artin\n",
    "- read soccer knowledge\n",
    "- analyze player data\n",
    "- use software tools\n",
    "- make coaching decisions\n",
    "- communicate with the player\n",
    "\n",
    "Today we build the first piece:\n",
    "> **The AI Agent.**"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## Phase 1 — What Is an AI Agent? 🤖\n",
    "\n",
    "An **AI Agent** goes beyond simple pattern recognition or text generation. While a traditional software script follows strict, predefined rules, an AI agent combines probabilistic reasoning with goal-driven action cycles.\n",
    "\n",
    "Key capabilities of an AI Agent include:\n",
    "1. **Perception:** Interpreting incoming raw data (e.g., video frames, tracking coordinates, physical metrics).\n",
    "2. **Reasoning:** Processing contextual rules, constraints, and tactical objectives.\n",
    "3. **Tool Use:** Querying specialized external software (e.g., databases, optical flow trackers, feature extractors).\n",
    "4. **Action:** Generating structured decisions, tactical reports, or interactive coaching feedback."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## Phase 2 — AI Model vs AI Agent\n",
    "\n",
    "### AI Model\n",
    "An AI model receives a prompt and generates text output based on trained statistical associations.\n",
    "\n",
    "**Example:**\n",
    "* **Player:** \"What should a winger do?\"\n",
    "* **AI Model:** \"A winger should create width, attack space, and support the attack.\"\n",
    "\n",
    "This response is useful, but generic. It lacks context regarding *who* is asking, their physical capabilities, or recent performance metrics.\n",
    "\n",
    "### AI Agent\n",
    "An AI agent operates within a functional feedback system:\n",
    "\n",
    "Goal → Reasoning → Tools → Information → Decision → Action\n",
    "\n",
    "```\n",
    "              ⚽ AI SOCCER COACH\n",
    "                       │\n",
    "             ┌─────────┴─────────┐\n",
    "             ↓                   ↓\n",
    "           GOAL                DATA\n",
    "             │                   │\n",
    "             └─────────┬─────────┘\n",
    "                       ↓\n",
    "                   AI MODEL\n",
    "                       ↓\n",
    "                 DECISION\n",
    "                       ↓\n",
    "                 COACHING\n",
    "                   ADVICE\n",
    "```\n",
    "\n",
    "**Core Distinction:** An AI model generates text. An AI agent integrates an AI model into an operational system capable of querying state data, evaluating progress against goals, and triggering software execution."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## Phase 3 — Build a Simple AI Coach\n",
    "\n",
    "We initialize our base Python environment and configure model connections. In this phase, we establish client instances and set up local environment variables securely.\n",
    "\n",
    "### 🔐 API Keys\n",
    "An API key grants your application authorized access to backend LLM interfaces. **Never expose or hardcode API keys in public repositories.** Always load credentials via environment variables (`os.environ`)."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import os\n",
    "import json\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "from google import genai\n",
    "from google.genai import types\n",
    "\n",
    "# Ensure GEMINI_API_KEY is set in environment\n",
    "if \"GEMINI_API_KEY\" not in os.environ:\n",
    "    os.environ[\"GEMINI_API_KEY\"] = \"YOUR_API_KEY_HERE\"\n",
    "\n",
    "client = genai.Client()\n",
    "print(\"✅ AI Soccer Coach client initialized!\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## Phase 4 — Give the Coach a Personality\n",
    "\n",
    "System instructions establish operational guardrails, tone, role, and domain expertise. By injecting system-level constraints, we instruct the model to adopt the role of a professional athletic coach and prohibit statistical hallucination."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "coach_instructions = \"\"\"\n",
    "You are the Artin FC AI Soccer Coach.\n",
    "\n",
    "Your job is to help a soccer player improve.\n",
    "\n",
    "You should:\n",
    "- Provide practical, high-performance soccer advice.\n",
    "- Explain your tactical and physical reasoning clearly.\n",
    "- Use player performance data whenever provided.\n",
    "- NEVER invent or hallucinate player statistics.\n",
    "- Clearly distinguish physical/tactical measurements from coaching recommendations.\n",
    "- Maintain an encouraging, analytical, and professional coaching tone.\n",
    "\"\"\"\n",
    "\n",
    "print(\"System instructions defined successfully.\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## Phase 5 — Ask the First Question\n",
    "\n",
    "We issue an initial query to test zero-shot model responses before introducing player-specific tracking telemetry."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "question = \"How can I improve as a winger?\"\n",
    "\n",
    "response = client.models.generate_content(\n",
    "    model=\"gemini-2.5-flash\",\n",
    "    contents=question,\n",
    "    config=types.GenerateContentConfig(\n",
    "        system_instruction=coach_instructions,\n",
    "        temperature=0.3\n",
    "    )\n",
    ")\n",
    "\n",
    "print(response.text)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "> **Teaching Insight:** The output provides general soccer fundamentals, but lacks knowledge of Artin's specific match metrics (e.g., top speed, stamina curve, positioning heatmap). To convert this model into a contextual agent, we must feed it real metrics generated during Mission 13."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## Phase 6 — Bring Mission 13 Back ⚽\n",
    "\n",
    "In Mission 13, computer vision scripts computed actual tracking parameters:\n",
    "- Total Distance Covered (yd)\n",
    "- Average Active Speed (yd/s)\n",
    "- Maximum Sprint Speed (yd/s)\n",
    "- Most Occupied Tactical Zone\n",
    "- Final-Third Occupancy Percentage (%)\n",
    "\n",
    "We construct a synthetic dataset mirroring the pandas DataFrame outputs generated in Mission 13."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Reconstructing actual physical metrics from Mission 13 CV pipeline\n",
    "artin_id = 4\n",
    "tracking_frames_count = 240  # 8 seconds @ 30 FPS\n",
    "total_distance_yards = 42.8\n",
    "average_speed = 3.85  # yd/s (~7.87 mph)\n",
    "maximum_speed = 7.60  # yd/s (~15.54 mph)\n",
    "most_common_zone = \"Final Third\"\n",
    "final_third_percentage = 68.5\n",
    "\n",
    "artin_data = {\n",
    "    \"player\": \"Artin\",\n",
    "    \"position\": \"Right Winger\",\n",
    "    \"tracking_id\": artin_id,\n",
    "    \"tracked_frames\": tracking_frames_count,\n",
    "    \"distance_yards\": round(total_distance_yards, 2),\n",
    "    \"average_speed\": round(average_speed, 2),\n",
    "    \"maximum_speed\": round(maximum_speed, 2),\n",
    "    \"most_occupied_zone\": most_common_zone,\n",
    "    \"final_third_percentage\": round(final_third_percentage, 1)\n",
    "}\n",
    "\n",
    "print(\"Artin Data Payload:\")\n",
    "print(json.dumps(artin_data, indent=2))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## Phase 7 — Build the First Coaching Tool 🛠️\n",
    "\n",
    "A **Tool** is a callable program function that exposes data retrieval or calculation endpoints to an execution pipeline."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def get_player_statistics():\n",
    "    \"\"\"Returns measured performance statistics for Artin from Mission 13.\"\"\"\n",
    "    return artin_data\n",
    "\n",
    "# Test tool execution\n",
    "player_stats = get_player_statistics()\n",
    "print(\"Tool output verification:\", player_stats)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## Phase 8 — Let the Agent Use the Tool\n",
    "\n",
    "We inject the output of `get_player_statistics()` directly into the agent's context prompt, forcing the LLM to ground its reasoning strictly on actual measurements."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "player_stats = get_player_statistics()\n",
    "\n",
    "coach_prompt = f\"\"\"\n",
    "Analyze this player's measured performance data:\n",
    "\n",
    "Player: {player_stats['player']}\n",
    "Position: {player_stats['position']}\n",
    "Distance Covered: {player_stats['distance_yards']} yards\n",
    "Average Speed: {player_stats['average_speed']} yards/second\n",
    "Maximum Speed: {player_stats['maximum_speed']} yards/second\n",
    "Most Occupied Zone: {player_stats['most_occupied_zone']}\n",
    "Final-Third Occupancy: {player_stats['final_third_percentage']}%\n",
    "\n",
    "Provide:\n",
    "1. Two movement strengths based on these numbers.\n",
    "2. Two physical/tactical areas to improve.\n",
    "3. One tactical recommendation.\n",
    "4. One training recommendation.\n",
    "\n",
    "Do not invent statistics. Clearly distinguish measurements from coaching recommendations.\n",
    "\"\"\"\n",
    "\n",
    "response = client.models.generate_content(\n",
    "    model=\"gemini-2.5-flash\",\n",
    "    contents=coach_prompt,\n",
    "    config=types.GenerateContentConfig(\n",
    "        system_instruction=coach_instructions,\n",
    "        temperature=0.2\n",
    "    )\n",
    ")\n",
    "\n",
    "print(response.text)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## Phase 9 — Build the Agent Loop 🔄\n",
    "\n",
    "The operational loop coordinates user intent, dynamic tool querying, state contextualization, and response synthesis:\n",
    "\n",
    "```\n",
    "        GOAL\n",
    "          ↓\n",
    "      UNDERSTAND\n",
    "          ↓\n",
    "       GET DATA  ──► (get_player_statistics)\n",
    "          ↓\n",
    "       ANALYZE\n",
    "          ↓\n",
    "       DECIDE\n",
    "          ↓\n",
    "       RESPOND\n",
    "```"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## Phase 10 — Build a Simple Coach Function\n",
    "\n",
    "We encapsulate the prompt composition, tool extraction, and LLM call inside a reusable, modular function."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def soccer_coach(question: str, player_data: dict) -> str:\n",
    "    \"\"\"\n",
    "    Processes player query using verified metrics through the AI Coach Agent.\n",
    "    \"\"\"\n",
    "    prompt = f\"\"\"\n",
    "Player Information:\n",
    "- Name: {player_data['player']}\n",
    "- Position: {player_data['position']}\n",
    "- Distance: {player_data['distance_yards']} yards\n",
    "- Average Speed: {player_data['average_speed']} yd/s\n",
    "- Maximum Speed: {player_data['maximum_speed']} yd/s\n",
    "- Most Occupied Zone: {player_data['most_occupied_zone']}\n",
    "- Final Third Occupancy: {player_data['final_third_percentage']}%\n",
    "\n",
    "Player Question: \"{question}\"\n",
    "\n",
    "Instruction: Answer directly as a professional soccer coach. Use supplied measurements accurately. Do not invent metrics.\n",
    "\"\"\"\n",
    "    response = client.models.generate_content(\n",
    "        model=\"gemini-2.5-flash\",\n",
    "        contents=prompt,\n",
    "        config=types.GenerateContentConfig(\n",
    "            system_instruction=coach_instructions,\n",
    "            temperature=0.2\n",
    "        )\n",
    "    )\n",
    "    return response.text\n",
    "\n",
    "print(\"soccer_coach function registered successfully.\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## Phase 11 — Create the Coach Conversation\n",
    "\n",
    "We test multi-turn queries against `soccer_coach()` using Artin's dataset."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "sample_questions = [\n",
    "    \"How did I perform?\",\n",
    "    \"What was my strongest area?\",\n",
    "    \"Where did I spend most of my time?\",\n",
    "    \"How can I improve as a winger?\",\n",
    "    \"What should I practice this week?\"\n",
    "]\n",
    "\n",
    "for idx, q in enumerate(sample_questions, 1):\n",
    "    print(f\"\\n--- Question {idx}: {q} ---\")\n",
    "    answer = soccer_coach(q, artin_data)\n",
    "    print(answer)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## 🏆 Challenge 1 — Ask Your Coach\n",
    "\n",
    "Evaluate whether the AI agent correctly grounds its evaluations on exact metrics (`42.8 yards`, `7.6 yd/s`, `68.5% Final Third`) without making up arbitrary statistics."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "challenge_1_q = \"Analyze my speed profile and tactical positioning. Am I pushing high enough up the pitch?\"\n",
    "print(soccer_coach(challenge_1_q, artin_data))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## 🏆 Challenge 2 — Add Another Tool\n",
    "\n",
    "Build a secondary tool function `get_zone_analysis()` that filters positional and field-occupancy telemetry."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def get_zone_analysis():\n",
    "    \"\"\"Tool function returning pitch location breakdown.\"\"\"\n",
    "    return {\n",
    "        \"most_occupied_zone\": artin_data[\"most_occupied_zone\"],\n",
    "        \"final_third_percentage\": artin_data[\"final_third_percentage\"],\n",
    "        \"defensive_third_percentage\": 5.2,\n",
    "        \"midfield_percentage\": 26.3\n",
    "    }\n",
    "\n",
    "zone_info = get_zone_analysis()\n",
    "print(\"Zone Analysis Tool Output:\", zone_info)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## ⭐ SUPER CHALLENGE — Performance Coach\n",
    "\n",
    "Build `get_performance_report()` to aggregate physical performance metrics into a standardized report structure."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def get_performance_report():\n",
    "    \"\"\"Generates a comprehensive player analytics summary.\"\"\"\n",
    "    stats = get_player_statistics()\n",
    "    zones = get_zone_analysis()\n",
    "    \n",
    "    report = {\n",
    "        \"summary_metrics\": stats,\n",
    "        \"spatial_distribution\": zones,\n",
    "        \"sprint_efficiency_score\": round((stats[\"maximum_speed\"] / stats[\"average_speed\"]), 2)\n",
    "    }\n",
    "    return report\n",
    "\n",
    "def run_performance_agent(user_query):\n",
    "    # Agent fetches data via tools\n",
    "    full_report = get_performance_report()\n",
    "    \n",
    "    agent_prompt = f\"\"\"\n",
    "Complete Performance Data:\n",
    "{json.dumps(full_report, indent=2)}\n",
    "\n",
    "User Request: {user_query}\n",
    "\n",
    "Synthesize the report and issue an elite-level athletic analysis.\n",
    "\"\"\"\n",
    "    res = client.models.generate_content(\n",
    "        model=\"gemini-2.5-flash\",\n",
    "        contents=agent_prompt,\n",
    "        config=types.GenerateContentConfig(\n",
    "            system_instruction=coach_instructions,\n",
    "            temperature=0.2\n",
    "        )\n",
    "    )\n",
    "    return res.text\n",
    "\n",
    "print(run_performance_agent(\"Give me my complete performance report.\"))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## Phase 12 — First Streamlit Agent 🖥️\n",
    "\n",
    "Below is the standalone Python script to launch the interactive **Artin FC AI Soccer Coach** web app in Streamlit.\n",
    "\n",
    "### Streamlit Application Code (`app.py`)\n",
    "Save the code block below into a file named `app.py` and run: `streamlit run app.py`"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "streamlit_app_code = \"\"\"import os\n",
    "import json\n",
    "import streamlit as st\n",
    "from google import genai\n",
    "from google.genai import types\n",
    "\n",
    "st.set_page_config(page_title=\"Artin FC AI Soccer Coach\", page_icon=\"⚽\", layout=\"centered\")\n",
    "\n",
    "st.title(\"⚽ ARTIN FC AI SOCCER COACH\")\n",
    "st.caption(\"Mission 14 — AI Agent Interface\")\n",
    "\n",
    "# Pre-loaded player telemetry from Mission 13\n",
    "artin_data = {\n",
    "    \"player\": \"Artin\",\n",
    "    \"position\": \"Right Winger\",\n",
    "    \"distance_yards\": 42.8,\n",
    "    \"average_speed\": 3.85,\n",
    "    \"maximum_speed\": 7.60,\n",
    "    \"most_occupied_zone\": \"Final Third\",\n",
    "    \"final_third_percentage\": 68.5\n",
    "}\n",
    "\n",
    "st.sidebar.header(\"👤 Player Profile\")\n",
    "st.sidebar.markdown(f\"**Player:** {artin_data['player']}\")\n",
    "st.sidebar.markdown(f\"**Position:** {artin_data['position']}\")\n",
    "st.sidebar.markdown(f\"**Distance:** {artin_data['distance_yards']} yards\")\n",
    "st.sidebar.markdown(f\"**Avg Speed:** {artin_data['average_speed']} yd/s\")\n",
    "st.sidebar.markdown(f\"**Top Speed:** {artin_data['maximum_speed']} yd/s\")\n",
    "st.sidebar.markdown(f\"**Primary Zone:** {artin_data['most_occupied_zone']}\")\n",
    "\n",
    "user_query = st.text_input(\"Ask your AI Coach:\", value=\"How did I perform in the final third?\")\n",
    "\n",
    "if st.button(\"Ask Coach\"):\n",
    "    if \"GEMINI_API_KEY\" not in os.environ:\n",
    "        st.error(\"API Key not found in environment variables!\")\n",
    "    else:\n",
    "        client = genai.Client()\n",
    "        system_instruction = \"\"\"\n",
    "        You are the Artin FC AI Soccer Coach. Provide tactical advice grounded strictly in supplied telemetry. Never hallucinate stats.\n",
    "        \"\"\"\n",
    "        prompt = f\"\"\"\n",
    "        Player Telemetry:\n",
    "        {json.dumps(artin_data, indent=2)}\n",
    "        \n",
    "        Question: {user_query}\n",
    "        \"\"\"\n",
    "        with st.spinner(\"Analyzing metrics...\"):\n",
    "            res = client.models.generate_content(\n",
    "                model=\"gemini-2.5-flash\",\n",
    "                contents=prompt,\n",
    "                config=types.GenerateContentConfig(\n",
    "                    system_instruction=system_instruction,\n",
    "                    temperature=0.2\n",
    "                )\n",
    "            )\n",
    "            st.markdown(\"### 🤖 AI Coach Advice\")\n",
    "            st.write(res.text)\n",
    "\"\"\"\n",
    "\n",
    "with open(\"app.py\", \"w\") as f:\n",
    "    f.write(streamlit_app_code)\n",
    "\n",
    "print(\"✅ Streamlit app script created successfully as app.py!\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## 🏆 Mission 14 Final Challenge\n",
    "\n",
    "Build your own version of the **Artin FC AI Soccer Coach**.\n",
    "\n",
    "### Verification Checklist:\n",
    "- [x] Accept a coaching question\n",
    "- [x] Configure system instructions defining the AI Coach persona\n",
    "- [x] Receive Artin's real tracking data from Mission 13\n",
    "- [x] Use Python functions as tools (`get_player_statistics`, `get_zone_analysis`)\n",
    "- [x] Analyze physical and tactical measurements\n",
    "- [x] Generate contextual coaching advice\n",
    "- [x] Strictly prohibit hallucinated statistics\n",
    "- [x] Deploy interactive UI in Streamlit"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## Final Reflection\n",
    "\n",
    "### Question 1: What is an AI model?\n",
    "*An AI model is a probabilistic algorithm trained to predict tokens or generate text/media based on learned statistical patterns.* \n",
    "\n",
    "### Question 2: What is an AI agent?\n",
    "*An AI agent is a goal-driven system that uses an AI model for reasoning while integrating tool execution, perception data, and multi-step decision loops.* \n",
    "\n",
    "### Question 3: What is a tool?\n",
    "*A tool is an executable function or API that allows an AI agent to fetch external data or trigger software actions.* \n",
    "\n",
    "### Question 4: Why shouldn't the AI invent Artin's statistics?\n",
    "*Hallucinated statistics lead to faulty coaching assessments, destroying trust and providing harmful physical or tactical guidance.* \n",
    "\n",
    "### Question 5: Complete\n",
    "- Mission 13 taught AI to **see** Artin.\n",
    "- Mission 14 taught AI to **understand** Artin's data.\n",
    "- Mission 15 will teach AI to **remember** Artin."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "# 🚀 What's Next?\n",
    "\n",
    "Our AI Coach can now analyze Artin.\n",
    "\n",
    "But there is a problem: every time we start a new conversation, the coach forgets everything. It doesn't remember:\n",
    "- Artin's previous conversations\n",
    "- previous training recommendations\n",
    "- previous performance\n",
    "- goals\n",
    "- preferences\n",
    "\n",
    "So our next challenge is:\n",
    "\n",
    "# 🧠 Mission 15: Give Your AI Coach a Memory\n",
    "\n",
    "We will teach our agent how to remember."
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
