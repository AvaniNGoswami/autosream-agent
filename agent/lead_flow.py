from agent.state import update_lead, is_lead_complete
from tools.lead_capture import mock_lead_capture

def handle_lead_flow(state, user_message):
    lead = state["lead"]
    if state.get("awaiting") is None:
        state["awaiting"] = "name"
        return "Great! Let's get you started. What's your name?"

    if state.get("awaiting") == "name":
        update_lead(state, "name", user_message)
        state["awaiting"] = "email"
        return "Thanks! What's your email?"

    if state.get("awaiting") == "email":
        update_lead(state, "email", user_message)
        state["awaiting"] = "platform"
        return "Great! Which platform do you create content on? (YouTube, Instagram)"


    if state.get("awaiting") == "platform":
        update_lead(state, "platform", user_message)

    if is_lead_complete(state):
        lead = state["lead"]

        mock_lead_capture(
            lead["name"],
            lead["email"],
            lead["platform"]
        )

        state["intent"] = None
        state["awaiting"] = None
        state["lead"] = {
            "name": None,
            "email": None,
            "platform": None
        }

        return "Awesome! You're all set. Our team will reach out to you shortly."

    return "Something went wrong. Let's try again."