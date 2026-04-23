# AutoStream - Social-to-Lead Agentic Workflow

## Overview
AutoStream is a conversational AI agent designed for a SaaS product that provides automated video editing tools.  
It can understand user intent, answer product queries using RAG, and convert high-intent users into qualified leads via tool execution.

The system is built using a modular agent architecture with LangGraph-based workflow orchestration.

---

## 1. How to Run the Project Locally

### 1. Clone Repository
git clone https://github.com/AvaniNGoswami/autosream-agent.git

cd autostream-agent

### Create Virtual Environment
python -m venv venv
source venv/bin/activate   # Mac/Linux

venv\Scripts\activate      # Windows

### Install Dependencies
pip install -r requirements.txt

### Setup Environment Variables
GEMINI_API_KEY=your_key_here

GROQ_API_KEY=your_key_here

### Run the Project
python main.py

## Architecture Explanation

The system is designed as a modular agentic workflow using LangGraph to manage multi-step reasoning and decision-making. Instead of a simple linear chatbot, the architecture follows a graph-based execution model where each node represents a specific responsibility such as intent detection, retrieval-augmented generation (RAG), or lead qualification.

LangGraph was chosen because it provides explicit control over state transitions, making it ideal for building structured AI agents that require multi-turn memory and tool execution. Unlike traditional chain-based frameworks, LangGraph allows conditional routing between nodes, which is essential for handling different user intents like greeting, product queries, and high-intent conversion flows.

State management is handled using a centralized dictionary-based structure that persists across interactions. It stores conversation history, detected intent, and lead information (name, email, platform). This ensures continuity across multiple turns and prevents loss of context during transitions between nodes.

The RAG pipeline uses FAISS with sentence embeddings to retrieve relevant product and policy information from a local knowledge base. The retrieved context is then passed to the LLM to generate grounded responses.

Overall, this architecture ensures scalability, modularity, and production-like behavior suitable for real-world AI agent deployment.

## WhatsApp Deployment (Webhook Integration)

To integrate this agent with WhatsApp, we would use the WhatsApp Business API (or Meta Cloud API) with a webhook-based architecture.

Flow:
WhatsApp user sends a message
Meta WhatsApp Cloud API forwards message to backend webhook
Flask/FastAPI server receives the message
Message is passed into LangGraph agent (graph.invoke(state))
Agent processes intent, RAG, or lead flow logic
Response is returned back to WhatsApp API
User receives AI-generated reply in chat
Technical Components:
Webhook server (FastAPI/Flask)
LangGraph agent engine
State store (Redis or in-memory for MVP)
WhatsApp Cloud API endpoint
Example Flow:

User -> WhatsApp -> Webhook -> Agent -> Response -> WhatsApp

## Key Features
- Intent classification (greeting / product / high-intent)
- RAG-based knowledge retrieval
- Multi-turn memory
- Lead capture tool execution
- Fallback LLM support (Gemini + Groq)
- LangGraph-based workflow orchestration
