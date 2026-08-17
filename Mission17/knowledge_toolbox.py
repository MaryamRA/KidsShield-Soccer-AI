def load_knowledge(filepath="soccer_knowledge.txt"):
    """
    Load soccer knowledge from a text file.

    Args:
        filepath: Path to the soccer knowledge file.

    Returns:
        The complete knowledge text, or an empty string if
        the file cannot be found.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return file.read()

    except FileNotFoundError:
        print(f"Knowledge file not found: {filepath}")
        return ""


def search_knowledge(knowledge, keyword):
    """
    Search soccer knowledge for paragraphs containing a keyword.

    Args:
        knowledge: Complete soccer knowledge text.
        keyword: Word or phrase to search for.

    Returns:
        A list of matching paragraphs.
    """
    if not knowledge:
        return []

    paragraphs = knowledge.split("\n\n")

    results = [
        paragraph
        for paragraph in paragraphs
        if keyword.lower() in paragraph.lower()
    ]

    return results


def get_tactical_knowledge(position, filepath="soccer_knowledge.txt"):
    """
    Retrieve soccer knowledge relevant to a player's position.

    Args:
        position: Player position such as Forward, Midfielder,
                  Defender, or Goalkeeper.
        filepath: Path to the soccer knowledge file.

    Returns:
        Relevant soccer knowledge as text.
    """
    knowledge = load_knowledge(filepath)

    if not knowledge:
        return "No soccer knowledge was found."

    results = search_knowledge(knowledge, position)

    if not results:
        return (
            f"No specific tactical knowledge was found for "
            f"the position: {position}"
        )

    return "\n\n".join(results)


def build_prompt(player_memory, team_data, retrieved_knowledge, question):
    """
    Build a coaching prompt using memory, team data,
    retrieved soccer knowledge, and the player's question.

    Args:
        player_memory: Persistent player memory.
        team_data: Player or team statistics.
        retrieved_knowledge: Relevant soccer knowledge.
        question: Player's coaching question.

    Returns:
        A complete prompt for the AI coach.
    """

    prompt = f"""
You are an AI Soccer Coach.

PLAYER MEMORY:
{player_memory}

TEAM STATS:
{team_data}

RETRIEVED SOCCER KNOWLEDGE:
{retrieved_knowledge}

PLAYER QUESTION:
{question}

Give personalized soccer advice.

Rules:
- Use the player's memory.
- Use the supplied performance data.
- Use the retrieved soccer knowledge.
- Do not invent statistics.
- Do not invent facts that are not present in the provided sources.
"""

    return prompt
