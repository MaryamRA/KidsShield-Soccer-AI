# ============================================================
# ⚽ MISSION 15
# memory_toolbox.py
#
# Memory tools for the AI Soccer Agent
# ============================================================

import json

MEMORY_FILE_NAME = "soccer_memory.json"

# ============================================================
# LOAD MEMORY SAFELY
# ============================================================

def load_memory():

    if os.path.exists(mt.MEMORY_FILE_NAME):

        return mt.recall()

    else:

        return {}


# ============================================================
# SAVE MEMORY
# ============================================================

def remember(memory, MEMORY_FILE_NAME):

    with open(MEMORY_FILE_NAME, "w") as file:
        json.dump(memory, file, indent=2)

    print("Soccer data saved!")

    return memory


# ============================================================
# LOAD MEMORY
# ============================================================

def recall():

    with open(MEMORY_FILE_NAME, "r") as file:
        memory = json.load(file)

    print("Soccer data loaded!")

    return memory


# ============================================================
# ADD DATA TO MEMORY
# ============================================================

def memorize(memory, key, value):

    if key not in memory:

        memory[key] = value

    elif isinstance(memory[key], list):

        if value not in memory[key]:

            memory[key].append(value)

        else:

            print(
                "This information is already in memory."
            )

            return memory

    else:

        memory[key] = value

    print("New information memorized!")

    return memory


# ============================================================
# REMOVE DATA FROM MEMORY
# ============================================================

def forget(memory, key, value=None):

    if key not in memory:

        print(
            "This information is not in memory."
        )

        return memory

    if isinstance(memory[key], list):

        if value in memory[key]:

            memory[key].remove(value)

            print(
                "Information forgotten!"
            )

        else:

            print(
                "This information is not in memory."
            )

    else:

        if value is None or memory[key] == value:

            del memory[key]

            print(
                "Information forgotten!"
            )

        else:

            print(
                "This information is not in memory."
            )

    return memory