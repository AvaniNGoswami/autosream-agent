from typing import TypedDict

from agent.intent import detect_intent
from agent.lead_flow import handle_lead_flow
from rag.rag_pipeline import generate_answer
from agent.state import is_lead_complete

from langgraph.graph import StateGraph, END


class AgentState(TypedDict):
    messages: list
    intent: str
    lead: dict
    awaiting: str
    response: str


def intent_node(state: AgentState):
    if state["intent"] == "high_intent" and not is_lead_complete(state):
        return state 

    user_message = state["messages"][-1]
    intent = detect_intent(user_message)
    state["intent"] = intent
    return state

def router_node(state: AgentState):
    intent = state["intent"]

    if intent == "greeting":
        state["response"] = "Hello! How can I help you today?"

    elif intent == "product_query":
        state["response"] = generate_answer(state["messages"][-1])

    elif intent == "high_intent":
        state["response"] = handle_lead_flow(state, state["messages"][-1])

    return state




def build_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("intent", intent_node)
    workflow.add_node("router", router_node)

    workflow.set_entry_point("intent")
    workflow.add_edge("intent", "router")
    workflow.add_edge("router", END)

    return workflow.compile()