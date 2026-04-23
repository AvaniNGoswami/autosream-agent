import json
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import google.generativeai as genai


from groq import Groq

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_llm = genai.GenerativeModel("gemini-1.5-flash")



embedder = SentenceTransformer("all-MiniLM-L6-v2")


with open("data/knowledge.json", "r") as f:
    data = json.load(f)


documents = [
    f"Basic plan: {data['pricing']['basic']}",
    f"Pro plan: {data['pricing']['pro']}",
    f"Refund policy: {data['policy']['refund']}",
    f"Support policy: {data['policy']['support']}"
]


embeddings = embedder.encode(documents)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

def retrieve(query, k=2):
    query_embedding = embedder.encode([query])
    distances, indices = index.search(np.array(query_embedding), k)

    results = [documents[i] for i in indices[0]]
    return results



def generate_answer(query):
    context = retrieve(query)

    prompt = f"""
You are a helpful SaaS assistant for AutoStream.

Use ONLY the context below to answer.

Context:
{context}

User Question:
{query}
"""

    try:
        response = gemini_llm.generate_content(prompt)
        return response.text

    except Exception as e:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content


