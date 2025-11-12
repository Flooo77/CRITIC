from datetime import datetime, timezone
from secrets import token_urlsafe
from sqlalchemy import Column, Boolean, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, mapped_column

from api.database import Base

def generate_session_token():
    return token_urlsafe(64)

class User(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True)
    username: str = Column(String, unique=True, index=True, nullable=False)
    hashed_password: str = Column(String, nullable=False)
    is_active: bool = Column(Boolean, default=False)
    is_local: bool = Column(Boolean, default=True)
    created_at: datetime = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    sessions = relationship("UserSession")

class UserSession(Base):
    __tablename__ = "user_sessions"

    id: int = Column(Integer, primary_key=True, index=True)
    value: str = Column(String, default=generate_session_token, nullable=False)
    created_at: datetime = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    expires_at: datetime = Column(DateTime, nullable=False)
    user_id: int = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="sessions")