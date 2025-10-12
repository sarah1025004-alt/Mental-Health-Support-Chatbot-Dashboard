# crud.py
from sqlalchemy.orm import Session
from models import User, ChatLog
from passlib.context import CryptContext
from typing import Optional, List

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, username: str, password: str, role: str = "user") -> User:
    hashed = pwd_context.hash(password)
    user = User(username=username, hashed_password=hashed, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def save_chat(db: Session, user_id: Optional[int], message: str, reply: str) -> ChatLog:
    chat = ChatLog(user_id=user_id, message=message, reply=reply)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat

def get_chats_for_user(db: Session, user_id: int, limit: int = 100) -> List[ChatLog]:
    return db.query(ChatLog).filter(ChatLog.user_id == user_id).order_by(ChatLog.created_at.desc()).limit(limit).all()

def list_recent_chats(db: Session, limit: int = 100) -> List[ChatLog]:
    return db.query(ChatLog).order_by(ChatLog.created_at.desc()).limit(limit).all()
