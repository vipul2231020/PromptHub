# PromptHub — AI Prompt Marketplace & Generator

A scalable backend system for managing, searching, and generating AI prompts using FastAPI, PostgreSQL, and NLP embeddings.

---

## Overview

PromptHub is an API-first backend that provides:

- Prompt marketplace with categories and collections
- Semantic search using embeddings
- Prompt generation using structured templates
- JWT-based authentication with role-based access
- Analytics for trending and usage tracking

---

## Architecture

Client → FastAPI → Service Layer → PostgreSQL + pgvector + Redis → Celery

---

## Features

### Authentication
- User registration and login
- JWT-based authentication
- Role-based access control (admin/user)

### Prompt Management
- Create, read, update, delete prompts
- Category and tag-based filtering
- Usage tracking and ratings

### Search
- Semantic search using vector embeddings
- Keyword fallback search

### Prompt Generation
- Template-based prompt generation
- Intent detection
- Prompt improvement pipeline

### Collections
- Group prompts into collections
- Admin-controlled creation

### Analytics
- Trending prompts
- Platform statistics

---

## Tech Stack

- FastAPI
- PostgreSQL (Supabase)
- SQLAlchemy
- JWT Authentication
- pgvector
- Redis
- Celery
- Sentence Transformers
- Docker

---

## Project Structure


prompthub/
│
├── app/
│ ├── api/
│ ├── core/
│ ├── db/
│ ├── models/
│ ├── schemas/
│ ├── services/
│ ├── main.py
│
├── worker/
├── scripts/
├── tests/
├── docker/
├── requirements.txt
├── .env


---

## Setup Instructions

### 1. Clone Repository


git clone https://github.com/vipul2231020/prompthub.git

cd prompthub


### 2. Create Virtual Environment


python -m venv venv
venv\Scripts\activate # Windows


### 3. Install Dependencies


pip install -r requirements.txt


### 4. Configure Environment Variables

Create `.env` file:


DATABASE_URL=postgresql+psycopg2://user:password@host:5432/db?sslmode=require
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30


---

## Running the Application

### Local Run


uvicorn app.main:app --reload


### API Docs 


http://127.0.0.1:8000/docs


---

## Database Seeding


python -m scripts.seed_prompts


---

## API Endpoints

| Method | Endpoint | Description |
|--------|---------|------------|
| POST | /auth/register | Register user |
| POST | /auth/login | Login and get token |
| GET | /prompts/ | List all prompts |
| POST | /prompts/ | Create prompt (admin) |
| GET | /prompts/{id} | Get prompt |
| PUT | /prompts/{id} | Update prompt |
| DELETE | /prompts/{id} | Delete prompt |
| GET | /collections/ | List collections |
| POST | /collections/ | Create collection (admin) |
| GET | /collections/{id} | Get collection |
| POST | /search/ | Semantic search |
| POST | /generate/ | Generate prompt |
| GET | /analytics/trending | Trending prompts |
| GET | /analytics/stats | Platform stats |

---

## Deployment

The backend is deployed on Render.

Start command:


uvicorn app.main:app --host 0.0.0.0 --port 10000

deployed api : https://prompthub-2ish.onrender.com/docs

---

## Testing


pytest tests/ -v