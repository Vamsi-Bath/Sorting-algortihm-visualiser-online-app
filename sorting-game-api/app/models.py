from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(40), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    class_name: Mapped[str] = mapped_column(String(10), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    games: Mapped[list["GameSession"]] = relationship(back_populates="user")

class GameSession(Base):
    __tablename__ = "game_sessions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    mode: Mapped[str] = mapped_column(String(40), nullable=False)
    insertion_correct: Mapped[int] = mapped_column(Integer, default=0)
    insertion_incorrect: Mapped[int] = mapped_column(Integer, default=0)
    bubble_correct: Mapped[int] = mapped_column(Integer, default=0)
    bubble_incorrect: Mapped[int] = mapped_column(Integer, default=0)
    final_score: Mapped[int] = mapped_column(Integer, default=0)
    is_finished: Mapped[bool] = mapped_column(Boolean, default=False)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    ended_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    user: Mapped[User] = relationship(back_populates="games")
    rounds: Mapped[list["Round"]] = relationship(back_populates="game", cascade="all, delete-orphan")

class Round(Base):
    __tablename__ = "rounds"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    game_session_id: Mapped[int] = mapped_column(ForeignKey("game_sessions.id"), nullable=False)
    sorting_type: Mapped[str] = mapped_column(String(20), nullable=False)
    question_type: Mapped[str] = mapped_column(String(30), nullable=False)
    original_array: Mapped[str] = mapped_column(Text, nullable=False)
    target_pass_number: Mapped[int] = mapped_column(Integer, nullable=False)
    target_array: Mapped[str] = mapped_column(Text, nullable=False)
    user_answer: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_correct: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    answered_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    game: Mapped[GameSession] = relationship(back_populates="rounds")
