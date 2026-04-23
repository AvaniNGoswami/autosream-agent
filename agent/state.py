def initialize_state():
    return {
        "intent": None,
        "messages": [],
        "lead": {
            "name": None,
            "email": None,
            "platform": None
        }
    }

def add_message(state, role, content):
    state["messages"].append({
        "role": role,
        "content": content
    })

def update_intent(state, intent):
    state["intent"] = intent

def update_lead(state, key, value):
    if key in state["lead"]:
        state["lead"][key] = value

def is_lead_complete(state):
    lead = state["lead"]
    return all([lead["name"], lead["email"], lead["platform"]])