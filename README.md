# Agentic AI Shopping Assistant

This microservice acts as the conversational AI shopping agent for the Ecommerce platform.

## Architecture
- **Framework**: FastAPI
- **LLM Orchestration**: LangGraph
- **Primary LLM Engine**: Groq (Llama 3 open-weight)
- **Vector Search**: PostgreSQL + pgvector
- **Short-Term Memory**: Redis

## Prerequisites
- Python 3.11+
- PostgreSQL with `pgvector` extension
- Redis
- Groq API Key
- Main Backend Service Token

## Setup
1. Clone the repository and navigate to `ai-assistant/`.
2. Copy `.env.example` to `.env` and fill in the required values.
3. Install dependencies:
   ```bash
   pip install -e .
   ```
4. Run database migrations:
   ```bash
   alembic upgrade head
   ```
5. Start the development server:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## Development Rules
- Do NOT directly access the main backend's business logic database tables.
- Always use `MainBackendClient` to fetch orders, products, etc.
- Adhere to the `AGENTS.md` guidelines for prompt engineering and agent boundaries.
