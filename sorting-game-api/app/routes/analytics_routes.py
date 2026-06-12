from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from ..auth import get_current_user
from ..database import get_db
from ..models import GameSession, User

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/classes")
def class_analytics(_: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.execute(
        select(User.class_name, func.count(GameSession.id), func.coalesce(func.avg(GameSession.final_score), 0))
        .join(GameSession, GameSession.user_id == User.id)
        .group_by(User.class_name)
        .order_by(User.class_name)
    ).all()
    return [{"class_name": r[0], "games_played": r[1], "average_score": round(float(r[2]), 2)} for r in rows]

@router.get("/sorting-types")
def sorting_type_analytics(_: User = Depends(get_current_user), db: Session = Depends(get_db)):
    totals = db.execute(
        select(
            func.coalesce(func.sum(GameSession.insertion_correct), 0),
            func.coalesce(func.sum(GameSession.insertion_incorrect), 0),
            func.coalesce(func.sum(GameSession.bubble_correct), 0),
            func.coalesce(func.sum(GameSession.bubble_incorrect), 0),
        )
    ).one()
    return {
        "insertion_correct": totals[0],
        "insertion_incorrect": totals[1],
        "bubble_correct": totals[2],
        "bubble_incorrect": totals[3],
    }
