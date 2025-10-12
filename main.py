# main.py
import os
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from typing import List


load_dotenv()
OPENAI_API_KEY = os.getenv("api-key")
from database import SessionLocal, engine, Base
import models, crud, ai, utils
from schemas import UserCreate, UserOut, ChatCreate, ChatOut

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="MindMate Backend - FastAPI")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"status": "MindMate backend is running 🚀"}

# Create user
@app.post("/create_user", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_username(db, user.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    u = crud.create_user(db, user.username, user.password)
    return u

# Basic authentication endpoint (demo only)
@app.post("/login", response_model=UserOut)
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if not db_user or not crud.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return db_user

# Save chat (manual)
@app.post("/save_chat", response_model=ChatOut)
def save_chat_endpoint(user_id: int = None, message: str = "", reply: str = "", db: Session = Depends(get_db)):
    if not message:
        raise HTTPException(status_code=400, detail="message required")
    chat = crud.save_chat(db, user_id, message, reply)
    return chat

# Get chats for a user
@app.get("/get_chats/{user_id}", response_model=List[ChatOut])
def get_chats(user_id: int, db: Session = Depends(get_db)):
    chats = crud.get_chats_for_user(db, user_id)
    return chats

# Get recent chats
@app.get("/recent_chats", response_model=List[ChatOut])
def recent_chats(limit: int = 50, db: Session = Depends(get_db)):
    return crud.list_recent_chats(db, limit=limit)

# Main chat endpoint: generates reply via OpenAI (if key set), saves chat, returns reply.
@app.post("/chat")
def chat_endpoint(payload: ChatCreate, db: Session = Depends(get_db)):
    if not payload.message or payload.message.strip() == "":
        raise HTTPException(status_code=400, detail="message required")

    # Crisis detection (basic)
    crisis = utils.detect_crisis(payload.message)
    if crisis:
        # immediate, safety-first reply
        urgent_reply = (
            "I'm very sorry you're feeling this way. If you are in immediate danger or might harm yourself, "
            "please contact your local emergency services right now or a suicide prevention hotline. "
            "If you want, I can provide crisis hotline numbers for your country or connect you with a counselor."
        )
        # Save chat with urgent reply
        chat = crud.save_chat(db, payload.user_id, payload.message, urgent_reply)
        return {"reply": urgent_reply, "chat_id": chat.id, "crisis": True}

    # Try OpenAI if configured
    reply = ai.call_openai_chat(payload.message)
    if reply is None:
        # Fallback canned reply if no API key provided
        reply = "Thanks for sharing. I'm here to listen — can you tell me a bit more about how you're feeling?"

    # Save and return
    chat = crud.save_chat(db, payload.user_id, payload.message, reply)
    return {"reply": reply, "chat_id": chat.id, "crisis": False}
