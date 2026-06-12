from fastapi import APIRouter, Depends
from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session
from ..auth import get_current_user
from ..database import get_db
from ..models import GameSession, User

router = APIRouter(prefix="/scores", tags=["scores"])

@router.get("/leaderboard")
def leaderboard(limit: int = 5, db: Session = Depends(get_db)):
    rows = db.execute(
        select(User.username, User.class_name, GameSession.final_score, GameSession.id)
        .join(GameSession, GameSession.user_id == User.id)
        .where(GameSession.final_score > 0)
        .order_by(desc(GameSession.final_score))
        .limit(limit)
    ).all()
    return [
        {"username": r[0], "class_name": r[1], "score": r[2], "game_id": r[3]}
        for r in rows
    ]

@router.get("/mine")
def my_scores(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    games = db.scalars(
        select(GameSession).where(GameSession.user_id == user.id).order_by(desc(GameSession.started_at)).limit(20)
    ).all()
    return [
        {
            "game_id": game.id,
            "mode": game.mode,
            "score": game.final_score,
            "started_at": game.started_at,
            "finished": game.is_finished,
        }
        for game in games
    ]
