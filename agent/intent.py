import os

from groq import Groq
import google.generativeai as genai
import json

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

def rule_based_intent(message: str):
    msg = message.lower()

    if any(word in msg for word in ["hi", "hello", "hey"]):
        return "greeting"

    if any(word in msg for word in ["buy", "subscribe", "sign up", "get started", "try pro"]):
        return "high_intent"

    if any(word in msg for word in ["price", "plan", "cost", "feature", "refund", "support"]):
        return "product_query"

    return None


def llm_intent(message: str):
    prompt = f"""
Classify the user intent into one of:
- greeting
- product_query
- high_intent

User: {message}

Return ONLY valid JSON:
{{ "intent": "greeting | product_query | high_intent" }}
"""
    try:
        response = gemini_model.generate_content(prompt)
        content = response.text.strip()
        content = content.replace("```json", "").replace("```", "").strip()

        return json.loads(content)["intent"]

    except Exception as e:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )

        content = response.choices[0].message.content.strip()

        content = content.replace("```json", "").replace("```", "").strip()

        return json.loads(content)["intent"]


def detect_intent(message: str):
    intent = rule_based_intent(message)

    if intent:
        return intent

    return llm_intent(message)