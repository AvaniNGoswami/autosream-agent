from agent.graph import build_graph

graph = build_graph()

state = {
    "messages": [],
    "intent": None,
    "lead": {
        "name": None,
        "email": None,
        "platform": None
    },
    "awaiting": None, 
    "response": ""
}

while True:
    user_input = input("User: ")

    state["messages"].append(user_input)

    state = graph.invoke(state)

    print("Bot:", state["response"])