def load_knowledge(filepath="soccer_knowledge.txt"):
    try:
        with open(filepath, "r") as file:
            return file.read()
    except FileNotFoundError:
        return ""

def search_knowledge(knowledge, keyword):
    if not knowledge:
        return []
    paragraphs = knowledge.split("\\n\\n")
    results = [p for p in paragraphs if keyword.lower() in p.lower()]
    return results

def build_prompt(player_memory, team_data, retrieved_knowledge, question):
    prompt = f"""\n You are an AI Soccer Coach.

    PLAYER MEMORY:
    {player_memory}

    TEAM STATS:
    {team_data}

    RETRIEVED SOCCER KNOWLEDGE:
    {retrieved_knowledge}

    PLAYER QUESTION:
    {question}

    Give personalized soccer advice. Use the player's memory, performance tracking data, and retrieved soccer knowledge.
    Do not invent statistics or facts not present in the provided sources.
    """
