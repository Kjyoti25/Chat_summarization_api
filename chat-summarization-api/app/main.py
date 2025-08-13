from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import chats, summaries, users
from app.websockets import summary as ws_summary
from app.config import settings

app = FastAPI(
    title="Chat Summarization API",
    description="API for chat storage and LLM-powered summarization",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chats.router, prefix="/chats", tags=["chats"])
app.include_router(summaries.router, prefix="/summaries", tags=["summaries"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(ws_summary.router, prefix="/ws", tags=["websocket"])