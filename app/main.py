from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings 
from app.core.logger import get_logger
from app.db.base import Base
from app.db.session import engine


from app.models import user, prompt, collection
from app.api.routes import auth, prompts, collections, search, generate, analytics

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application shut down and startup events."""

    logger.info("PromptHub setting up.....")
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database created......")

    yield
    logger.info("PromptHub shutting down.....")

app = FastAPI(
    title="PromptHub API",
    description="AI-powered Prompt Marketplace, Generator & Vault",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(prompts.router)
app.include_router(collections.router)
app.include_router(search.router)
app.include_router(generate.router)
app.include_router(analytics.router)


@app.get("/", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": "1.0.0",
    }


@app.get("/health", tags=["Health"])
def detailed_health():
    return {
        "status": "ok",
        "database": "connected",
        "app": settings.APP_NAME,
    }
