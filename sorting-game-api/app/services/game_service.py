import json
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models import GameSession, Round, User
from .sorting_service import GeneratedRound, generate_round
from .scoring_service import calculate_score

TIME_LIMIT_SECONDS = 30

def make_round_response(game: GameSession, round_: Round) -> dict:
    original = json.loads(round_.original_array)
    target = json.loads(round_.target_array)
    if round_.question_type == "ARRANGE_TO_PASS":
        prompt = f"Arrange the bars into pass {round_.target_pass_number} of {round_.sorting_type.replace('_', ' ').title()}."
        target_array = None
        target_pass_number = round_.target_pass_number
    else:
        prompt = f"Type which pass number creates the array shown for {round_.sorting_type.replace('_', ' ').title()}."
        target_array = target
        target_pass_number = None
    return {
        "game_id": game.id,
        "round_id": round_.id,
        "mode": game.mode,
        "sorting_type": round_.sorting_type,
        "question_type": round_.question_type,
        "original_array": original,
        "target_pass_number": target_pass_number,
        "target_array": target_array,
        "prompt": prompt,
        "time_limit_seconds": TIME_LIMIT_SECONDS,
    }

def create_round(db: Session, game: GameSession) -> Round:
    generated: GeneratedRound = generate_round(game.mode)
    round_ = Round(
        game_session_id=game.id,
        sorting_type=generated.sorting_type,
        question_type=generated.question_type,
        original_array=json.dumps(generated.original_array),
        target_pass_number=generated.target_pass_number,
        target_array=json.dumps(generated.target_array),
    )
    db.add(round_)
    db.commit()
    db.refresh(round_)
    return round_

def start_game(db: Session, user: User, mode: str) -> tuple[GameSession, Round]:
    game = GameSession(user_id=user.id, mode=mode)
    db.add(game)
    db.commit()
    db.refresh(game)
    round_ = create_round(db, game)
    return game, round_

def submit_answer(db: Session, user: User, round_id: int, answer_array: list[int] | None, answer_pass_number: int | None):
    round_ = db.get(Round, round_id)
    if not round_:
        raise HTTPException(status_code=404, detail="Round not found")
    game = db.get(GameSession, round_.game_session_id)
    if not game or game.user_id != user.id:
        raise HTTPException(status_code=403, detail="This round does not belong to you")
    if game.is_finished:
        raise HTTPException(status_code=400, detail="Game is already finished")
    if round_.is_correct is not None:
        raise HTTPException(status_code=400, detail="Round has already been answered")

    expected_array = json.loads(round_.target_array)
    expected_pass = round_.target_pass_number
    if round_.question_type == "ARRANGE_TO_PASS":
        correct = answer_array == expected_array
        round_.user_answer = json.dumps(answer_array or [])
    else:
        correct = answer_pass_number == expected_pass
        round_.user_answer = str(answer_pass_number)

    round_.is_correct = correct
    round_.answered_at = datetime.now(timezone.utc)

    if round_.sorting_type == "BUBBLE_SORT":
        if correct:
            game.bubble_correct += 1
        else:
            game.bubble_incorrect += 1
    else:
        if correct:
            game.insertion_correct += 1
        else:
            game.insertion_incorrect += 1

    game.final_score = calculate_score(
        game.insertion_correct,
        game.insertion_incorrect,
        game.bubble_correct,
        game.bubble_incorrect,
    )
    next_round = create_round(db, game)
    db.commit()
    db.refresh(game)
    return game, round_, next_round, correct, expected_array, expected_pass

def finish_game(db: Session, user: User, game_id: int) -> GameSession:
    game = db.get(GameSession, game_id)
    if not game or game.user_id != user.id:
        raise HTTPException(status_code=404, detail="Game not found")
    game.is_finished = True
    game.ended_at = datetime.now(timezone.utc)
    game.final_score = calculate_score(
        game.insertion_correct,
        game.insertion_incorrect,
        game.bubble_correct,
        game.bubble_incorrect,
    )
    db.commit()
    db.refresh(game)
    return game
