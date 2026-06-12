from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..auth import get_current_user
from ..database import get_db
from ..models import User
from ..schemas import FinishGameResponse, StartGameRequest, SubmitAnswerRequest, SubmitAnswerResponse, RoundResponse
from ..services.game_service import finish_game, make_round_response, start_game, submit_answer
from ..services.scoring_service import counters_dict

router = APIRouter(prefix="/games", tags=["games"])

@router.post("/start", response_model=RoundResponse)
def start(payload: StartGameRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    game, round_ = start_game(db, user, payload.mode)
    return make_round_response(game, round_)

@router.post("/{game_id}/submit-answer", response_model=SubmitAnswerResponse)
def submit(game_id: int, payload: SubmitAnswerRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    game, answered_round, next_round, correct, expected_array, expected_pass = submit_answer(
        db, user, payload.round_id, payload.answer_array, payload.answer_pass_number
    )
    return {
        "correct": correct,
        "expected_array": expected_array,
        "expected_pass_number": expected_pass,
        "score": game.final_score,
        "counters": counters_dict(game),
        "next_round": make_round_response(game, next_round),
    }

@router.post("/{game_id}/finish", response_model=FinishGameResponse)
def finish(game_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    game = finish_game(db, user, game_id)
    return {"game_id": game.id, "final_score": game.final_score, "counters": counters_dict(game)}
