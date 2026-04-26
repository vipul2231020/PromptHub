# 🚀 PromptHub — AI Prompt Marketplace + Generator

> Scalable AI-powered prompt marketplace with semantic search, prompt generation,
> and collection-based discovery using FastAPI, PostgreSQL, and NLP embeddings.

## 🏗️ Architecture
Client → FastAPI → Services → PostgreSQL + pgvector + Redis → Celery


## ⚡ Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/yourname/prompthub
cd prompthub
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
2. Configure Environment
Copy code
cp .env.example .env
# Edit .env with your database and secret key settings
3. Run with Docker (Recommended)
Copy code
docker-compose -f docker/docker-compose.yml up --build
4. Run Locally
Copy code
# Start PostgreSQL and Redis first, then:
uvicorn app.main:app --reload
5. Seed Database
Copy code
python -m scripts.seed_prompts
6. Run Tests
Copy code
pytest tests/ -v
📡 API Endpoints
⎘ Copy table
Method	Endpoint	Description
POST	/auth/register	Register user
POST	/auth/login	Login → JWT token
GET	/prompts/	List all prompts
GET	/prompts/{id}	Get single prompt
POST	/prompts/	Create prompt (admin)
GET	/collections/	List collections
GET	/collections/{id}	Get collection
POST	/search/	Semantic search
POST	/generate/	Generate AI prompt
GET	/analytics/trending	Trending prompts
GET	/analytics/stats	Platform stats
🌐 Interactive Docs
After starting the server:

Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc
🛠️ Tech Stack
FastAPI — High-performance API framework
PostgreSQL + pgvector — Database with vector similarity search
Redis — Caching and message broker
Celery — Background task processing
Sentence Transformers — NLP embeddings (all-MiniLM-L6-v2)
Docker — Containerization


---

## 🎯 How to Run Everything (Step by Step)

```bash
# Step 1: Docker (easiest)
docker-compose -f docker/docker-compose.yml up --build

# Step 2: Seed data
docker exec prompthub_api python -m scripts.seed_prompts

# Step 3: Open API docs
# http://localhost:8000/docs

# ─────────────────────────────
# OR run locally:

# Step 1: Install deps
pip install -r requirements.txt

# Step 2: Set env
cp .env .env  # edit DATABASE_URL

# Step 3: Start server
uvicorn app.main:app --reload

# Step 4: Seed
python -m scripts.seed_prompts

# Step 5: Run tests
pytest tests/ -v
🧠 Project Understanding Summary
⎘ Copy table
Layer	What It Does
Auth	JWT login/register, admin roles
Prompt Service	Full CRUD, category filtering, usage tracking
Search Service	pgvector semantic search, ILIKE fallback
AI Service	Intent detection → template → tone improvement
Template Engine	9 structured templates for different intents
Celery Worker	Background embedding generation
Seed Script	100 prompts, 5 categories, 5 collections
Tests	Auth, Prompts, Analytics with SQLite in-memory
This is a complete, production-ready backend system ready for deployment!